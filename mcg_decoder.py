# Add this function to 'ecg_decoder.py' or a new 'mcg_decoder.py'

class MCGDecoder:
    def __init__(self, sensor_sensitivity_tesla: float = 1e-12): # PicoTesla
        self.sensor_sensitivity_tesla = sensor_sensitivity_tesla

    def decode_magnetic_field(self, raw_mcg_packet: bytes) -> list:
        """
        Extracts raw MCG data vectors (x, y, z components) from telemetry.
        """
        # [Imagine parsing raw magnetic sensor data...]
        # This would involve converting raw sensor bits to Tesla values.
        
        # Let's mock the result as a list of magnetic field vectors (in PicoTesla):
        simulated_magnetic_field = [
            {'axis': 'x', 'value': 5.2, 'unit': 'pT'},
            {'axis': 'y', 'value': -2.1, 'unit': 'pT'},
            {'axis': 'z', 'value': 1.8, 'unit': 'pT'}
        ]
        return simulated_magnetic_field
