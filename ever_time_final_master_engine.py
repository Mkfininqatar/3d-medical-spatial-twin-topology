import numpy as np
import matplotlib.pyplot as plt

class AnatomicalNode:
    def __init__(self, name, triangles, role):
        self.name = name
        self.triangles = triangles
        self.role = role
        self.signal_output = 0.0

    def process_signal(self, input_signal):
        # Base processing logic for each region
        self.signal_output = input_signal * 1.025  # Telemetry amplification/routing factor
        return self.signal_output

class EverTimeTelemetryPipeline:
    def __init__(self):
        # Initializing Anatomical Parts with their functional roles & mesh metrics
        self.heart = AnatomicalNode("Heart (Cardio Chamber)", 48000, "Generates 72 BPM rhythm & Red Phase Wave Doppler hydrodynamics.")
        self.hindbrain = AnatomicalNode("Hindbrain (Brainstem)", 48320, "Autonomic regulation & initial cardiac-respiratory signal capture.")
        self.thalamus = AnatomicalNode("Thalamus", 40532, "Sensory relay node: filters and routes bio-signals to higher centers.")
        self.cerebrum = AnatomicalNode("Cerebrum (Telencephalon)", 54708, "High-level cognitive processing and sovereign telemetry state mapping.")
        self.cerebellum = AnatomicalNode("Cerebellum", 54708, "Motor control telemetry, rhythm coordination, and micro-signal balancing.")
        self.spinal_cord = AnatomicalNode("Spinal Cord & Nerves", 41280, "Signal transmission highway connecting peripheral telemetry array.")
        
        self.base_bpm = 72.0

    def simulate_signal_propagation(self, duration_seconds=3, sampling_rate=100):
        time_steps = np.linspace(0, duration_seconds, duration_seconds * sampling_rate)
        
        # 1. Heart generates the primary 72 BPM cardiac pulse (Red Phase Wave)
        cardiac_raw = self.base_bpm + 15 * np.sin(2 * np.pi * (self.base_bpm / 60) * time_steps)
        
        hindbrain_signals = []
        thalamus_signals = []
        cerebrum_signals = []
        cerebellum_signals = []

        for val in cardiac_raw:
            # Signal Flow: Heart -> Hindbrain -> Thalamus -> Cerebrum/Cerebellum
            sig_hb = self.hindbrain.process_signal(val)
            sig_th = self.thalamus.process_signal(sig_hb)
            sig_cb = self.cerebrum.process_signal(sig_th)
            sig_cer = self.cerebellum.process_signal(sig_th)
            
            hindbrain_signals.append(sig_hb)
            thalamus_signals.append(sig_th)
            cerebrum_signals.append(sig_cb)
            cerebellum_signals.append(sig_cer)

        return time_steps, cardiac_raw, np.array(hindbrain_signals), np.array(thalamus_signals), np.array(cerebrum_signals), np.array(cerebellu_signals if 'cerebellu_signals' in locals() else cerebellum_signals)

    def render_signal_processing_dashboard(self):
        t, heart, hb, th, cb, cer = self.simulate_signal_propagation()

        plt.style.use('dark_background')
        fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)

        # Plot 1: Heart & Hindbrain Synchronization
        axes[0].plot(t, heart, color='#FF2400', linewidth=2.5, label='Heart: 72 BPM (Red Phase Wave)')
        axes[0].plot(t, hb, color='#FF1493', linewidth=1.8, linestyle='--', label='Hindbrain: Autonomic Capture')
        axes[0].set_title("EVER-TIME Sovereign Engine: Cardio-Neural Signal Pipeline", fontsize=13, color='white', fontweight='bold')
        axes[0].legend(loc='upper right')
        axes[0].grid(True, color='#333333', linestyle=':')

        # Plot 2: Thalamus Filtering & Relay
        axes[1].plot(t, th, color='#00CC99', linewidth=2.0, label='Thalamus: Sensory Relay Node')
        axes[1].set_ylabel("Amplitude (mV)", color='white')
        axes[1].legend(loc='upper right')
        axes[1].grid(True, color='#333333', linestyle=':')

        # Plot 3: Cerebrum & Cerebellum Distributed Telemetry
        axes[2].plot(t, cb, color='#FF6600', linewidth=2.0, label='Cerebrum: Cognitive Processing Node')
        axes[2].plot(t, cer, color='#9933CC', linewidth=2.0, linestyle='-.', label='Cerebellum: Rhythm Coordination Node')
        axes[2].set_xlabel("Timeline (Seconds)", color='white')
        axes[2].legend(loc='upper right')
        axes[2].grid(True, color='#333333', linestyle=':')

        plt.tight_layout()
        plt.savefig("cardio_neural_signal_processing.png", dpi=300)
        print("[SUCCESS] Cardio-Neural Signal Processing Dashboard generated successfully for My Lab by Abdul Majeed!")
        plt.show()

if __name__ == "__main__":
    pipeline = EverTimeTelemetryPipeline()
    pipeline.render_signal_processing_dashboard()
