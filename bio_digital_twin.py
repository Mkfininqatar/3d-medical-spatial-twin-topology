import time
import math
import logging
from dataclasses import dataclass, field
from typing import Dict, Any, Optional

# Configure telemetry logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("BioDigitalTwinEngine")

@dataclass
class SystemState:
    external_input_audio: float = 1.0  # 1.0 = 100% active (Ear/Microphone)
    external_input_visual: float = 1.0 # 1.0 = 100% active (Eye/Camera)
    internal_echo_heart: float = 1.0   # Internal cardiac electromagnetic resonance
    memory_rendering: bool = True      # Internal visualization/caching
    speed_object: float = 0.0          # Object velocity (m/s)
    speed_vehicle: float = 0.0         # Vehicle velocity (m/s)
    passing_distance: float = 0.0      # Spatial clearance (meters)
    is_terminated: bool = False        # Ultimate system shutdown (Death/Ruh Journey)

class BioDigitalTwinSystem:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.state = SystemState()
        logger.info(f"Initialized Bio-Digital Twin Node: {self.node_id}")

    def update_sensors(self, audio_active: bool, visual_active: bool) -> None:
        """Simulates cutting off external sensory inputs (Ear/Eye)."""
        self.state.external_input_audio = 1.0 if audio_active else 0.0
        self.state.external_input_visual = 1.0 if visual_active else 0.0

    def compute_signal_frequency(self) -> float:
        """
        Calculates active system frequency based on inputs:
        - Loss of audio cuts ~98% of external frequency flow.
        - Loss of visual cuts remaining external feed.
        - Preserves the baseline 2% internal echo signal driven by the heart.
        """
        if self.state.is_terminated:
            return 0.0

        # External weight calculation
        ext_audio_weight = 0.98
        ext_visual_weight = 0.02
        
        external_factor = (
            (self.state.external_input_audio * ext_audio_weight) + 
            (self.state.external_input_visual * ext_visual_weight)
        )
        
        # If external inputs are completely dead (0.0), check internal echo loop
        if external_factor == 0.0:
            if self.state.internal_echo_heart > 0.0 and self.state.memory_rendering:
                # Internal eco signal remains active (Heart resonance & internal rendering)
                return 0.02  
            return 0.0
            
        return external_factor

    def evaluate_collision_risk(self, v_obj: float, v_veh: float, distance: float) -> Dict[str, Any]:
        """Evaluates collision probability based on speed disparity and proximity."""
        self.state.speed_object = v_obj
        self.state.speed_vehicle = v_veh
        self.state.passing_distance = distance

        if self.state.external_input_visual == 0.0:
            return {
                "status": "BLIND_SPOT",
                "risk": "CRITICAL",
                "message": "Visual gateway closed. Object telemetry data cannot reach sub-hub."
            }

        relative_speed = abs(self.state.speed_vehicle - self.state.speed_object)
        reaction_threshold = 1.5  # seconds

        if self.state.passing_distance <= (relative_speed * reaction_threshold):
            return {
                "status": "COLLISION_IMMINENT",
                "risk": "FATAL",
                "message": "Insufficient passing distance and speed clearance. Accident triggered."
            }
        
        return {
            "status": "SAFE",
            "risk": "NOMINAL",
            "message": "Trajectory clearance optimal."
        }

    def execute_legacy_shutdown(self) -> None:
        """Simulates the final terminal event (Ruh journey transition)."""
        logger.info("Executing ultimate system lifecycle boundary (Ruh journey initiated)...")
        self.state.external_input_audio = 0.0
        self.state.external_input_visual = 0.0
        self.state.internal_echo_heart = 0.0
        self.state.memory_rendering = False
        self.state.is_terminated = True
        logger.info("System state fully transitioned. Legacy code artifacts preserved.")

if __name__ == "__main__":
    twin = BioDigitalTwinSystem("HPC-Cardio-Neural-Node-01")

    # Scenario 1: Normal Operation
    freq = twin.compute_signal_frequency()
    logger.info(f"Active Signal Frequency Level: {freq * 100}%")

    # Scenario 2: External Inputs Disabled (Audio & Visual Cut)
    twin.update_sensors(audio_active=False, visual_active=False)
    residual_freq = twin.compute_signal_frequency()
    logger.info(f"Isolated State Residual Echo Frequency: {residual_freq * 100}% (Driven by Heart)")

    # Scenario 3: Collision Evaluation
    risk_assessment = twin.evaluate_collision_risk(v_obj=12.5, v_veh=25.0, distance=3.0)
    logger.info(f"Collision Assessment: {risk_assessment}")

    # Scenario 4: Terminal Legacy Transition
    twin.execute_legacy_shutdown()
