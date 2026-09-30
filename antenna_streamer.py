"""
Antenna telemetry streaming layer.

Current implementation:
- Simulation backend
- Deterministic/controlled synthetic waveform generation
- Async streaming interface
- Designed so a real hardware backend can be added later

Important:
This module does NOT currently read physical antenna hardware.
"""

import asyncio
import logging
import time
from typing import AsyncGenerator, Optional

import numpy as np


logger = logging.getLogger("AntennaStreamer")


class MiddleAntennaClient:
    """
    Antenna telemetry client.

    The current backend is synthetic simulation.
    A real HTTP/socket/serial backend can later implement the
    same public interface.
    """

    def __init__(
        self,
        antenna_ip: str = "192.168.1.100",
        port: int = 8080,
        polling_rate_hz: float = 60.0,
        seed: Optional[int] = 42,
    ):
        if polling_rate_hz <= 0:
            raise ValueError("polling_rate_hz must be greater than zero")

        self.antenna_ip = antenna_ip
        self.port = port
        self.antenna_address = (
            f"http://{antenna_ip}:{port}/live/telemetry"
        )

        self.polling_rate_hz = float(polling_rate_hz)

        self.is_connected = False
        self.mode = "simulation"

        self.rng = np.random.default_rng(seed)

        self.samples_generated = 0
        self.start_time = None

    # ------------------------------------------------------------------
    # Connection
    # ------------------------------------------------------------------

    async def connect_hardware(self):
        """
        Start the simulation backend.

        No physical hardware connection is performed here.
        """

        if self.is_connected:
            return

        logger.info(
            "Starting antenna telemetry backend | mode=%s",
            self.mode,
        )

        # Simulated initialization delay.
        await asyncio.sleep(0.05)

        self.is_connected = True
        self.start_time = time.perf_counter()

        logger.info(
            "Antenna telemetry stream initialized | "
            "rate=%.2f Hz | backend=%s",
            self.polling_rate_hz,
            self.mode,
        )

    # ------------------------------------------------------------------
    # Synthetic signal generation
    # ------------------------------------------------------------------

    def _generate_simulated_batch(
        self,
        batch_size: int,
    ) -> np.ndarray:
        """
        Generate synthetic 3-channel telemetry.

        Shape:
            (batch_size, 3)

        Channels are generic simulation channels.
        They must NOT be interpreted as validated ECG/EEG/MCG
        channels without an actual acquisition specification.
        """

        if batch_size <= 0:
            raise ValueError(
                "batch_size must be greater than zero"
            )

        # White-noise component.
        noise = self.rng.normal(
            loc=0.0,
            scale=0.05,
            size=(batch_size, 3),
        )

        # Time base for this block.
        sample_indices = np.arange(
            self.samples_generated,
            self.samples_generated + batch_size,
            dtype=np.float64,
        )

        t = sample_indices / self.polling_rate_hz

        # Low-frequency synthetic waveform.
        cardiac_component = np.sin(
            2.0 * np.pi * 1.0 * t
        )

        # Secondary component.
        neural_component = 0.35 * np.sin(
            2.0 * np.pi * 8.0 * t
        )

        waveform = (
            cardiac_component
            + neural_component
        )

        # Broadcast the simulated signal across 3 channels.
        signal_block = waveform[:, None] * np.array(
            [1.0, 0.8, 0.6],
            dtype=np.float64,
        )

        signal_block += noise

        self.samples_generated += batch_size

        return signal_block.astype(np.float32)

    # ------------------------------------------------------------------
    # Streaming
    # ------------------------------------------------------------------

    async def generate_live_magnetic_waves(
        self,
        batch_size: int = 100,
    ) -> AsyncGenerator[np.ndarray, None]:
        """
        Asynchronously generate synthetic telemetry batches.

        This preserves the same interface that a future real
        hardware backend can use.
        """

        if not self.is_connected:
            await self.connect_hardware()

        interval = 1.0 / self.polling_rate_hz

        while self.is_connected:

            loop_start = time.perf_counter()

            batch = self._generate_simulated_batch(
                batch_size=batch_size
            )

            yield batch

            elapsed = time.perf_counter() - loop_start

            sleep_duration = max(
                0.0,
                interval - elapsed,
            )

            await asyncio.sleep(sleep_duration)

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def get_status(self) -> dict:
        """
        Return stream diagnostics.
        """

        elapsed = None

        if self.start_time is not None:
            elapsed = (
                time.perf_counter()
                - self.start_time
            )

        return {
            "connected": self.is_connected,
            "mode": self.mode,
            "endpoint": self.antenna_address,
            "polling_rate_hz": self.polling_rate_hz,
            "samples_generated": self.samples_generated,
            "runtime_seconds": elapsed,
        }

    # ------------------------------------------------------------------
    # Disconnect
    # ------------------------------------------------------------------

    async def disconnect_hardware(self):
        """
        Stop the telemetry stream.

        Current implementation only stops the simulation backend.
        """

        if not self.is_connected:
            return

        self.is_connected = False

        logger.info(
            "Antenna telemetry stream stopped."
        )


# ----------------------------------------------------------------------
# Standalone test
# ----------------------------------------------------------------------

async def _demo():
    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s "
            "[%(levelname)s] "
            "%(name)s: %(message)s"
        ),
    )

    client = MiddleAntennaClient(
        polling_rate_hz=60.0,
        seed=42,
    )

    await client.connect_hardware()

    try:
        stream = client.generate_live_magnetic_waves(
            batch_size=20
        )

        for _ in range(5):
            batch = await stream.__anext__()

            logger.info(
                "Received simulated batch | "
                "shape=%s | dtype=%s | "
                "min=%.4f | max=%.4f",
                batch.shape,
                batch.dtype,
                float(batch.min()),
                float(batch.max()),
            )

    finally:
        await client.disconnect_hardware()


if __name__ == "__main__":
    asyncio.run(_demo())
