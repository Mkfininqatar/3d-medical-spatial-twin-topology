"""
Module: smart_hospital_iort.py
Purpose: IoT & IoRT (Internet of Medical Things / Internet of Robotic Things) real-time 
         data ingestion pipeline for the 3D Medical Spatial Twin.
Author: Abdul Mazed Hossain | QID: 29205036405
"""

import time
import json
import logging
from typing import Dict, Any

logger = logging.getLogger("smart_hospital_iort")

class SmartHospitalIoRTPipeline:
    """Manages real-time UWB positioning, robotic surgical tools, and IoT patient wearables."""
    def __init__(self, facility_id: str, operating_room: str):
        self.facility_id = facility_id
        self.operating_room = operating_room
        self.device_registry = {}

    def register_device(self, device_id: str, device_type: str) -> None:
        """Registers an IoRT node or wearable sensor into the spatial topology."""
        self.device_registry[device_id] = {
            "type": device_type,
            "status": "active",
            "connected_at": time.time_ns() // 1_000
        }
        logger.info(f"Registered IoRT Device [{device_id}] of type '{device_type}' in {self.operating_room}")

    def ingest_sensor_stream(self, device_id: str, spatial_coords: dict, telemetry_payload: dict) -> Dict[str, Any]:
        """Ingests live asynchronous UWB positioning and telemetry data."""
        if device_id not in self.device_registry:
            self.register_device(device_id, "unclassified_sensor")

        packet = {
            "facility_id": self.facility_id,
            "or_room": self.operating_room,
            "device_id": device_id,
            "coordinates_xyz": spatial_coords,
            "sensor_data": telemetry_payload,
            "ingest_timestamp_us": time.time_ns() // 1_000
        }
        return packet

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | [IoRT-ENGINE] | %(levelname)s | %(message)s")
    
    pipeline = SmartHospitalIoRTPipeline(facility_id="DOHA-MED-HUB-01", operating_room="OR-SUITE-B")
    pipeline.register_device("ROB-ARM-MICRON-X1", "surgical_robot")
    pipeline.register_device("UWB-TAG-PATIENT-09", "wearable_telemetry")

    stream_packet = pipeline.ingest_sensor_stream(
        device_id="ROB-ARM-MICRON-X1",
        spatial_coords={"x": 12.45, "y": 3.82, "z": 1.15},
        telemetry_payload={"actuator_torque_nm": 0.42, "precision_error_mm": 0.012}
    )

    print("\n--- SMART HOSPITAL IoRT STREAM PACKET ---")
    print(json.dumps(stream_packet, indent=2))
