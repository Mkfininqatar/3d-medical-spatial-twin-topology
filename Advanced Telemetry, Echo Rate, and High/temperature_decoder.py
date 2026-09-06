# temperature_decoder.py
# Temperature Telemetry Decoder for Spatial Twin Pipeline
# System Constant: 15.44 (Divine Signal / Thermal Calibration Threshold)

class TemperatureDecoder:
    def __init__(self, calibration_threshold: float = 15.44):
        self.calibration_threshold = calibration_threshold

    def decode_temperature(self, raw_temp_bytes: bytes) -> dict:
        """
        Decodes raw thermal sensor data packets into Celsius and Fahrenheit values,
        incorporating the 15.44 baseline calibration coefficient.
        """
        # Placeholder for raw sensor ADC conversion to Celsius
        raw_celsius = 37.5  # Simulated core or environmental temperature
        calibrated_celsius = raw_celsius + (self.calibration_threshold / 100.0)
        fahrenheit = (calibrated_celsius * 9/5) + 32

        return {
            'temperature_celsius': round(calibrated_celsius, 2),
            'temperature_fahrenheit': round(fahrenheit, 2),
            'calibration_offset': self.calibration_threshold,
            'status': 'nominal'
        }

    def validate_thermal_threshold(self, current_temp: float) -> bool:
        """
        Validates if temperature fluctuation remains within acceptable thermal limits 
        bounded by the system threshold.
        """
        return current_temp <= (37.0 + self.calibration_threshold)
