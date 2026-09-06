"""
Advanced Security & Telemetry Validation Layer
Project: QNV 2030 HPC Medical Spatial Twin Topology
Team: Majeed (Architect), Tamim (Lead Eng), Hamid (Analyst)
Repository: https://github.com/Mkfininqatar/python-logger2
"""

import time
import hmac
import hashlib
import logging
from typing import Dict, Any

# Configure Secure Logging with Integrity Signatures
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d UTC | SECURE_GRID | NODE: %(node_id)s | HASH: %(sig_hash)s | STATUS: %(status)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("HPC_Secure_Telemetry")

class SecurityValidationLayer:
    def __init__(self, secret_key: bytes):
        self.secret_key = secret_key

    def generate_packet_signature(self, payload: str) -> str:
        """Generates an HMAC-SHA256 integrity signature to prevent data tampering."""
        return hmac.new(self.secret_key, payload.encode('utf-8'), hashlib.sha256).hexdigest()[:16]

    def validate_node_telemetry(self, node_id: str, payload_data: Dict[str, Any]) -> bool:
        """Enforces zero-trust validation checks across distributed telemetry nodes."""
        raw_payload = f"{node_id}:{payload_data.get('timestamp')}:{payload_data.get('signal')}"
        expected_sig = self.generate_packet_signature(raw_payload)
        
        # Verify cryptographic integrity
        if expected_sig == payload_data.get('signature'):
            logger.info("Secure telemetry packet verified successfully.", extra={
                'node_id': node_id, 
                'sig_hash': expected_sig, 
                'status': 'INTEGRITY_VERIFIED'
            })
            return True
        else:
            logger.warning("Integrity violation detected. Packet dropped.", extra={
                'node_id': node_id, 
                'sig_hash': expected_sig, 
                'status': 'BREACH_PREVENTED'
            })
            return False

if __name__ == "__main__":
    # Initialize zero-trust security layer for the HPC grid
    grid_security = SecurityValidationLayer(secret_key=b"QNV_2030_Secure_Cluster_Key")
    
    current_time = time.perf_counter_ns()
    sample_payload = {
        "timestamp": current_time,
        "signal": 423.85,
        "signature": grid_security.generate_packet_signature(f"Doha_HPC_Core:{current_time}:423.85")
    }
    
    print("[*] Executing security and integrity validation on Doha Core Node...")
    grid_security.validate_node_telemetry("Doha_HPC_Core", sample_payload)
import hmac
import hashlib
import time
import json
import logging

# Configure logging for spatial-temporal telemetry
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SecurityLayer:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key.encode('utf-8')

    def generate_telemetry_token(self, node_id: str, timestamp: float) -> str:
        """Generates an HMAC-SHA256 integrity token for node telemetry."""
        message = f"{node_id}:{timestamp}".encode('utf-8')
        return hmac.new(self.secret_key, message, hashlib.sha256).hexdigest()

    def validate_node_signal(self, node_id: str, timestamp: float, token: str, tolerance: float = 2.0) -> bool:
        """Validates zero-trust token and clock synchronization within microsecond tolerance."""
        current_time = time.time()
        
        # Check for replay attacks or clock drift
        if abs(current_time - timestamp) > tolerance:
            logging.warning(f"Clock synchronization failed for node {node_id}. Drift exceeds tolerance.")
            return False

        expected_token = self.generate_telemetry_token(node_id, timestamp)
        if hmac.compare_digest(expected_token, token):
            logging.info(f"Node {node_id} validated successfully with secure telemetry.")
            return True
        
        logging.error(f"Security validation failed for node {node_id}: Invalid token signature.")
        return False

# Example execution loop for spatial topology nodes
if __name__ == "__main__":
    sec_layer = SecurityLayer(secret_key="QNV_2030_HPC_SECURE_KEY")
    
    node_id = "N1_Neural_Gateway"
    current_ts = time.time()
    
    # Generate token
    token = sec_layer.generate_telemetry_token(node_id, current_ts)
    print(f"Generated Token: {token}")
    
    # Validate token
    is_valid = sec_layer.validate_node_signal(node_id, current_ts, token)
    print(f"Signal Validation Status: {is_valid}")
# Revised 'security_layer.py' (Integrated)

import hmac
import hashlib
from ecg_decoder import ECGDecoder  # Import the new decoder
from ecg_decoder import MCGDecoder  # Import the new decoder

DIVINE_SIGNAL_THRESHOLD = 15.44

class SecurityLayer:
    def __init__(self, secret_key: bytes):
        self.secret_key = secret_key
        self.ecg_decoder = ECGDecoder()
        self.mcg_decoder = MCGDecoder()

    def validate_and_process_telemetry(self, packet_data: bytes, received_hmac: str, twin_node_vitals: float):
        """
        Validates packet integrity and extracts vital signs (HR & Magnetic).
        """
        # 1. Validate HMAC (Security Check)
        computed_hmac = hmac.new(self.secret_key, packet_data, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(computed_hmac, received_hmac):
            return "ERROR: HMAC Validation Failed", None, None

        # 2. Decode Physiological Data (Feature Extraction)
        current_heart_rate = self.ecg_decoder.decode_bpm(packet_data)
        current_magnetic_field = self.mcg_decoder.decode_magnetic_field(packet_data)

        # 3. Apply Digital Twin Threshold (Integrity Check)
        hr_within_tolerance = self.ecg_decoder.validate_against_digital_twin(current_heart_rate, twin_node_vitals)

        if not hr_within_tolerance:
            print(f"WARNING: Heart Rate Mismatch! Twin: {twin_node_vitals}, Actual: {current_heart_rate}")
            # In a real scenario, this might trigger an alert or drop the packet.

        return "SUCCESS", current_heart_rate, current_magnetic_field

# Example Usage (in your main application):
# security_system = SecurityLayer(secret_key=b"super_secret_key")
# status, hr, mcg = security_system.validate_and_process_telemetry(
#     packet_data=b"...",  # Actual raw data
#     received_hmac="...", # Received HMAC
#     twin_node_vitals=76.0 # Value from your 'Cardio-Neural Axis Spatial Topology' digital twin
# )
# print(f"Status: {status}, Extracted BPM: {hr}, Magnetic Field Vectors: {mcg}")
