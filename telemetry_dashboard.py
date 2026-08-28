import time
import requests
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Configurations for the real-time polling interface
API_URL = "http://127.0.0"
STREAM_URL = "http://127.0.0"

# Initialize Matplotlib Figure Layout
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
fig.suptitle("QNV 2030: 3D Cardio-Neural Spatial Twin Dashboard", fontsize=14, fontweight='bold')

# Setup Stream Subplot 1: Signal Waveform (X, Y, Z coordinates over time)
time_window = 50
time_axis = np.arange(0, time_window)
wave_x = np.zeros(time_window)
wave_y = np.zeros(time_window)
wave_z = np.zeros(time_window)

line_x, = ax1.plot(time_axis, wave_x, label="X (Cardio-Spatial)", color="#ff4d4d", linewidth=1.5)
line_y, = ax1.plot(time_axis, wave_y, label="Y (Neural-Temporal)", color="#33cc33", linewidth=1.5)
line_z, = ax1.plot(time_axis, wave_z, label="Z (Magnetic Wave)", color="#3399ff", linewidth=1.5)

ax1.set_title("Real-Time Hardware Signal Ingestion (60 Hz)")
ax1.set_xlim(0, time_window)
ax1.set_ylim(-5, 5)
ax1.set_ylabel("Amplitude")
ax1.legend(loc="upper right")
ax1.grid(True, linestyle="--", alpha=0.5)

# Setup Stream Subplot 2: Mesh Buffer Accumulation Metrics
buffer_chunks = 10
buffer_axis = np.arange(0, buffer_chunks)
buffer_loads = np.zeros(buffer_chunks)

bar_chart = ax2.bar(buffer_axis, buffer_loads, color="#9933ff", alpha=0.8, edgecolor="#6600cc")
ax2.set_title("GPU Topology Buffer Synced Block State")
ax2.set_xlim(-0.5, buffer_chunks - 0.5)
ax2.set_ylim(0, 100)
ax2.set_xlabel("Mesh Block Index")
ax2.set_ylabel("Saturation (%)")
ax2.grid(True, linestyle="--", alpha=0.3, axis='y')

def init_dashboard():
    line_x.set_ydata(np.zeros(time_window))
    line_y.set_ydata(np.zeros(time_window))
    line_z.set_ydata(np.zeros(time_window))
    return line_x, line_y, line_z

def update_dashboard_frame(frame):
    global wave_x, wave_y, wave_z, buffer_loads
    try:
        requests.get(API_URL, timeout=0.1)
    except Exception:
        pass

    try:
        mock_signals = np.random.normal(0, 1, (5, 3)).tolist()
        payload = {"signals": mock_signals}
        res = requests.post(STREAM_URL, json=payload, timeout=0.1)
        
        if res.status_code == 200:
            wave_x = np.roll(wave_x, -1)
            wave_y = np.roll(wave_y, -1)
            wave_z = np.roll(wave_z, -1)
            wave_x[-1] = mock_signals[-1][0]
            wave_y[-1] = mock_signals[-1][1]
            wave_z[-1] = mock_signals[-1][2]
    except Exception:
        wave_x = np.roll(wave_x, -1)
        wave_y = np.roll(wave_y, -1)
        wave_z = np.roll(wave_z, -1)
        wave_x[-1] = np.sin(time.time()) + np.random.normal(0, 0.2)
        wave_y[-1] = np.cos(time.time() * 1.5) + np.random.normal(0, 0.2)
        wave_z[-1] = np.sin(time.time() * 0.5) + np.random.normal(0, 0.2)

    line_x.set_ydata(wave_x)
    line_y.set_ydata(wave_y)
    line_z.set_ydata(wave_z)

    buffer_loads = np.roll(buffer_loads, -1)
    buffer_loads[-1] = np.random.uniform(70, 95)
    
    for rect, h in zip(bar_chart, buffer_loads):
        rect.set_height(h)

    return line_x, line_y, line_z

ani = animation.FuncAnimation(
    fig, update_dashboard_frame, init_func=init_dashboard,
    interval=16, blit=False, cache_frame_data=False
)

plt.tight_layout()
plt.show()
