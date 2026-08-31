cat << 'EOF' > hpc_telemetry.py
import numpy as np
import time

class CardioNeuralTelemetryFilter:
    def __init__(self, process_variance=1e-5, measurement_variance=1e-2):
        self.q = process_variance
        self.r = measurement_variance
        self.x_est = 0.0
        self.p_est = 1.0

    def adaptive_kalman_update(self, raw_signal):
        """Adaptive Kalman Filter for Corrupted Signal Restoration"""
        x_pred = self.x_est
        p_pred = self.p_est + self.q

        k_gain = p_pred / (p_pred + self.r)
        self.x_est = x_pred + k_gain * (raw_signal - x_pred)
        self.p_est = (1 - k_gain) * p_pred
        
        return self.x_est

    def pll_frequency_correction(self, brain_phase, heart_phase, base_freq, kp=0.5):
        """PLL Frequency Synchronization & Drift Correction"""
        freq_diff = (1.0 / (2.0 * np.pi)) * (brain_phase - heart_phase)
        corrected_freq = base_freq - (kp * freq_diff)
        return float(corrected_freq)

    def detect_corruption(self, signal_series, current_val):
        """Threshold-based 3-Sigma Anomaly Detection"""
        if len(signal_series) < 10:
            return "Stable"
            
        mean_val = np.mean(signal_series)
        std_val = np.std(signal_series)
        
        if std_val == 0:
            return "Stable"
            
        z_score = abs(current_val - mean_val) / std_val
        if z_score > 3.0:
            return "Corrupted/Out of Control"
        return "Stable"

if __name__ == "__main__":
    telemetry_filter = CardioNeuralTelemetryFilter()
    signal_buffer = []
    
    print("Initializing HPC Cardio-Neural Telemetry Engine with Anti-Corruption Filter...")
    
    for i in range(15):
        raw_val = 1.25 + (0.1 * np.sin(i)) if i != 10 else 6.5 
        
        status = telemetry_filter.detect_corruption(signal_buffer, raw_val)
        
        if status == "Corrupted/Out of Control":
            print(f"[WARNING] Anomaly detected at step {i}: {raw_val}. Applying Kalman restoration...")
            processed_val = telemetry_filter.adaptive_kalman_update(raw_val)
        else:
            processed_val = telemetry_filter.adaptive_kalman_update(raw_val)
            signal_buffer.append(raw_val)
            if len(signal_buffer) > 50:
                signal_buffer.pop(0)

        print(f"Step {i:02d} | Status: {status:<25} | Processed Signal: {processed_val:.4f}")
        time.sleep(0.1)
EOF
