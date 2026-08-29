<<<<<<< HEAD
 
=======
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

# Page Configuration
st.set_page_config(
    page_title="3D Medical Spatial Twin Topology",
    page_icon="🫀",
    layout="wide"
)

st.title("🫀 3D Medical Spatial Twin Topology Dashboard")
st.markdown("Real-time HPC Telemetry & Cardio-Neural Spatial Mapping Engine.")

# Sidebar Controls
st.sidebar.header("Simulation Parameters")
node_count = st.sidebar.slider("Spatial Nodes Count", min_value=100, max_value=2000, value=500, step=100)
update_speed = st.sidebar.slider("Telemetry Refresh Rate (s)", min_value=0.5, max_value=3.0, value=1.0, step=0.5)
run_simulation = st.sidebar.checkbox("Run Real-Time Telemetry Stream", value=False)

# Initialize Session State for Coordinates
if 'coords' not in st.session_state or len(st.session_state.coords) != node_count:
    st.session_state.coords = np.random.uniform(-50.0, 50.0, (node_count, 3))

# Main Dashboard Layout
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("Interactive 3D Spatial Topology Matrix")
    plot_placeholder = st.empty()

with col2:
    st.subheader("HPC Telemetry Metrics")
    metric_dispersion = st.empty()
    metric_nodes = st.empty()
    metric_status = st.empty()

# Function to render Plotly 3D scatter plot
def render_3d_topology(coordinates):
    fig = go.Figure(data=[go.Scatter3d(
        x=coordinates[:, 0],
        y=coordinates[:, 1],
        z=coordinates[:, 2],
        mode='markers',
        marker=dict(
            size=4,
            color=coordinates[:, 2], # Color intensity based on Z-axis depth
            colorscale='Viridis',
            opacity=0.8
        )
    )])
    
    fig.update_layout(
        scene=dict(
            xaxis_title='X Spatial Axis (mm)',
            yaxis_title='Y Spatial Axis (mm)',
            zaxis_title='Z Cardio-Neural Depth (mm)'
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        height=600
    )
    return fig

# Initial Render
current_fig = render_3d_topology(st.session_state.coords)
plot_placeholder.plotly_chart(current_fig, use_container_width=True)

# Metrics update
diff = st.session_state.coords[:, np.newaxis, :] - st.session_state.coords[np.newaxis, :, :]
max_disp = np.max(np.linalg.norm(diff, axis=-1))

metric_dispersion.metric("Max Spatial Dispersion", f"{max_disp:.2f} mm")
metric_nodes.metric("Active Spatial Nodes", f"{node_count}")
metric_status.metric("Engine Status", "Standby" if not run_simulation else "Streaming...")

# Real-time Simulation Loop
if run_simulation:
    while run_simulation:
        # Simulate organic spatial shifting
        st.session_state.coords += np.random.normal(0, 0.8, st.session_state.coords.shape)
        
        # Re-render plot and metrics
        updated_fig = render_3d_topology(st.session_state.coords)
        plot_placeholder.plotly_chart(updated_fig, use_container_width=True)
        
        diff = st.session_state.coords[:, np.newaxis, :] - st.session_state.coords[np.newaxis, :, :]
        max_disp = np.max(np.linalg.norm(diff, axis=-1))
        metric_dispersion.metric("Max Spatial Dispersion", f"{max_disp:.2f} mm")
        metric_status.metric("Engine Status", "Live Telemetry Active")
        
        time.sleep(update_speed)
        st.rerun()
import streamlit as st
import requests

st.set_page_config(page_title="3D Medical Spatial Twin Dashboard", layout="wide")

st.title("🧬 3D Medical Spatial Twin Topology Dashboard")
st.subheader("Cardio-Neural Axis Mapping & Telemetry Simulation")

# FastAPI ব্যাকএন্ডের সাথে কানেক্ট করার চেষ্টা
try:
    response = requests.get("http://127.0.0").json()
    st.success(f"Backend Connected: {response['service']}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Synchronization", value=response["synchronization_metric"])
    with col2:
        st.metric(label="Cumulative Drift", value=f"{response['cumulative_drift_us']} μs")
    with col3:
        st.metric(label="Location", value=response["processing_node"])
except:
    st.warning("FastAPI ব্যাকএন্ড সার্ভারটি চালু নেই। অনুগ্রহ করে অন্য টার্মিনালে `uvicorn main:app --reload` রান করুন।")
import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time

st.set_page_config(page_title="3D Medical Spatial Twin Dashboard", layout="wide", page_icon="🧬")

st.title("🧬 3D Medical Spatial Twin Topology Dashboard")
st.subheader("Cardio-Neural Axis Mapping & Telemetry Simulation (HPC Core)")

# সেশন স্টেটে ডেটা হিস্ট্রি ট্র্যাক করার জন্য
if "telemetry_history" not in st.session_state:
    st.session_state.telemetry_history = []

# ১. ব্যাকএন্ড থেকে ডেটা ফেচ করা
BACKEND_URL = "http://127.0.0.1:8000"

try:
    # হোম রুট থেকে মেইন ইনফো নেওয়া
    root_info = requests.get(f"{BACKEND_URL}/").json()
    # টেলিমেট্রি রুট থেকে সিন্ক ডেটা নেওয়া
    telemetry_resp = requests.get(f"{BACKEND_URL}/api/telemetry/sync").json()
    
    st.success(f"⚡ Connected to HPC Backend Node: {root_info['location']}")
    
    # মেট্রিstatics রো
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Mesh Faces", f"{root_info['mesh_specs']['faces']:,}")
    col2.metric("Mesh Vertices", f"{root_info['mesh_specs']['vertices']:,}")
    col3.metric("Sync Drift", f"{telemetry_resp['cumulative_drift_us']} μs")
    col4.metric("Status", "ONLINE", delta="Healthy")
    
    # ডেটা হিস্ট্রি আপডেট (টাইম-সিরিজ চার্টের জন্য)
    current_time = time.strftime("%H:%M:%S")
    st.session_state.telemetry_history.append({
        "Time": current_time, 
        "Drift": telemetry_resp['cumulative_drift_us'],
        "Load": np.random.uniform(40, 85) # HPC Load Simulation
    })
    if len(st.session_state.telemetry_history) > 20:
        st.session_state.telemetry_history.pop(0)
        
    df_history = pd.DataFrame(st.session_state.telemetry_history)

    # ড্যাশবোর্ড লেআউট: ৩ডি গ্রাফ এবং টেলিমেট্রি চার্ট
    left_col, right_col = st.columns([1, 1])
    
    with left_col:
        st.write("### 🌐 Spatial-Temporal 3D Mesh Topology")
        # কার্ডিও-নিউরাল অ্যাক্সিসের ৩ডি নোড সিমুলেশন
        n_nodes = 200
        z_axis = np.linspace(-5, 5, n_nodes)
        x_axis = np.sin(z_axis * 2) * np.exp(-np.abs(z_axis)*0.1)
        y_axis = np.cos(z_axis * 2) * np.exp(-np.abs(z_axis)*0.1)
        
        fig_3d = go.Figure(data=[go.Scatter3d(
            x=x_axis, y=y_axis, z=z_axis,
            mode='markers+lines',
            marker=dict(size=4, color=z_axis, colorscale='Viridis', opacity=0.8),
            line=dict(color='cyan', width=2)
        )])
        fig_3d.update_layout(margin=dict(l=0, r=0, b=0, t=0), template="plotly_dark")
        st.plotly_chart(fig_3d, use_container_width=True)

    with right_col:
        st.write("### 📈 Real-Time HPC Telemetry Streams")
        fig_line = px.line(df_history, x="Time", y="Load", title="HPC Node Computing Load (%)")
        fig_line.update_layout(template="plotly_dark")
        st.plotly_chart(fig_line, use_container_width=True)
        
    # অটো-রিফ্রেশ মেকানিজম (লাইভ ডেটা স্ট্রিমিংয়ের জন্য)
    time.sleep(1)
    st.rerun()

except Exception as e:
    st.error("❌ Failed to connect to the FastAPI Backend Server.")
    st.info("দয়া করে আরেকটি টার্মিনালে `uvicorn main:app --reload` কমান্ডটি চালু রাখুন।")
>>>>>>> 30fdc9ad3172d6a6c0b3b488333e8894eef25a0e
import logging
from flask import Flask, jsonify, request
# Importing the newly integrated high-performance engine
from medical_topology import CardioNeuralTopologyEngine

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Global engine instance to persist the 1.88M face mesh buffer across API calls
topology_engine = CardioNeuralTopologyEngine()

# =====================================================================
# Your previous endpoints, decorators, or custom middleware remain unaltered here
# ... (RESOLVED MERGE CONFLICTS FROM PREVIOUS BASE CODE) ...
# =====================================================================

@app.route('/api/telemetry/stream', methods=['POST'])
def stream_telemetry():
    """
    Resolved conflict endpoint for streaming real-time Middle Antenna signal data
    into the updated spatial twin topology matrix.
    """
    try:
        data = request.get_json()
        if not data or 'signals' not in data:
            return jsonify({"status": "error", "message": "Missing 'signals' array data"}), 400
        
        # Extracted signals from network payload
        raw_signals = data['signals']
        
        # Updating the 1.88M faces mesh topology layout via the high-performance engine
        updated_buffer = topology_engine.run_telemetry_pipeline(raw_signals)
        
        return jsonify({
            "status": "success",
            "message": "Spatial twin topology updated successfully",
            "buffer_shape": updated_buffer.shape
        }), 200

    except Exception as e:
        logging.error(f"Error updating spatial twin topology inside app.py: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/topology/status', methods=['GET'])
def get_topology_status():
    """
    Retrieves system health metrics for the Cardio-Neural mesh.
    """
    return jsonify({
        "engine_active": True,
        "target_faces": topology_engine.num_faces,
        "target_vertices": topology_engine.num_vertices,
        "buffer_status": "synced"
    }), 200

if __name__ == '__main__':
    # =====================================================================
    # Your previous server port configs/configurations remain here
    # =====================================================================
    app.run(host='0.0.0.0', port=5000, debug=True)
import logging
import requests  # Required to call the geolocation API
from flask import Flask, jsonify, request
from medical_topology import CardioNeuralTopologyEngine

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

topology_engine = CardioNeuralTopologyEngine()

def get_country_from_ip(ip_address):
    """
    Fetches the country name from an incoming IP address using a free geolocation API.
    Handles local development IPs safely.
    """
    # Safeguard for local testing (localhost / private network IPs)
    if ip_address in ['127.0.0.1', 'localhost'] or ip_address.startswith('192.168.'):
        return "Local Network / Development Environment"
        
    try:
        # Calling free geolocation API
        response = requests.get(f"http://ip-api.com{ip_address}", timeout=2)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                return data.get('country', 'Unknown Country')
    except Exception as geo_error:
        logging.error(f"Failed to resolve geolocation for IP {ip_address}: {str(geo_error)}")
        
    return "Unknown Location"

@app.route('/api/telemetry/stream', methods=['POST'])
def stream_telemetry():
    """
    Updated streaming endpoint that captures the viewer's IP address 
    and identifies their country of origin before processing data.
    """
    try:
        # Capturing the incoming client remote IP address
        # Handles reverse proxies using X-Forwarded-For if deployed on cloud
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        
        # Resolving country name from the captured IP
        viewer_country = get_country_from_ip(client_ip)
        
        # Logging the country info natively into your spatial twin console
        logging.info(f"[TRAFFIC] Incoming telemetry stream from Country: {viewer_country} (IP: {client_ip})")
        
        data = request.get_json()
        if not data or 'signals' not in data:
            return jsonify({"status": "error", "message": "Missing 'signals' array data"}), 400
        
        raw_signals = data['signals']
        updated_buffer = topology_engine.run_telemetry_pipeline(raw_signals)
        
        return jsonify({
            "status": "success",
            "message": "Spatial twin topology updated successfully",
            "detected_origin": viewer_country,
            "buffer_shape": updated_buffer.shape
        }), 200

    except Exception as e:
        logging.error(f"Error inside app.py: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
import time
import asyncio
import random
import streamlit as st
import pandas as pd

# --- STREAMLIT PAGE CONFIG ---
st.set_page_config(
    page_title="Brain Underpass Engine - Live Telemetry",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Brain Underpass Engine: Live Spatial Telemetry")
st.markdown("Real-time high-frequency neural antenna tracking and processing throughput.")

# --- INITIALIZE CORE ENGINE STATE ---
if "resting_potential_mv" not in st.session_state:
    st.session_state.resting_potential_mv = -70.0
    st.session_state.action_potential_mv = 30.0

# --- PLACEHOLDERS FOR LIVE UI ELEMENTS ---
metrics_row = st.columns(3)
with metrics_row[0]:
    tps_metric = st.empty()
with metrics_row[1]:
    total_metric = st.empty()
with metrics_row[2]:
    active_route_metric = st.empty()

st.divider()

chart_row = st.columns([2, 1])
with chart_row[0]:
    st.subheader("📈 Live Voltage Activity (mV)")
    chart_placeholder = st.empty()
with chart_row[1]:
    st.subheader("📋 Latest Telemetry Syncs")
    table_placeholder = st.empty()

# --- BACKEND TELEMETRY PROCESSING ENGINE ---
def validate_and_filter(raw_signal_input):
    """Validates and clamps incoming voltage thresholds."""
    if not isinstance(raw_signal_input, (int, float)):
        return 0.0
    return max(0.0, min(float(raw_signal_input), 1.0))

def process_signal(raw_signal, signal_id):
    """Processes signal micro-payload mapping."""
    clean_signal = validate_and_filter(raw_signal)
    
    if clean_signal > 0.5:
        current_mv = st.session_state.action_potential_mv
        route_status = "EXPRESS_BYPASS"
    else:
        current_mv = st.session_state.resting_potential_mv
        route_status = "RESTING_DEFAULT"

    return {
        "Signal ID": signal_id,
        "Input": round(clean_signal, 3),
        "Voltage (mV)": current_mv,
        "Routing Path": route_status,
        "Timestamp": time.strftime("%H:%M:%S")
    }

# --- CONTROL PANEL & STREAM RUNNER ---
st.sidebar.header("🎛️ Control Panel")
stream_active = st.sidebar.toggle("Start Live Stream", value=True)
sim_speed = st.sidebar.slider("Signal Generation Speed", min_value=10, max_value=200, value=80, step=10, help="Signals generated per batch frame")

if stream_active:
    # Historical tracking for live charts (keeps last 50 data points)
    history_buffer = deque = []
    total_processed = 0
    
    # Simple loop simulation matching Streamlit execution context
    while stream_active:
        start_frame_time = time.time()
        
        # Simulate an incoming burst batch of raw signal data (including spatial noise/corrupted tags)
        raw_batch = [random.uniform(0.0, 1.1) if random.random() > 0.05 else "corrupted_noise" for _ in range(sim_speed)]
        
        batch_payloads = []
        express_count = 0
        
        for sig in raw_batch:
            total_processed += 1
            payload = process_signal(sig, total_processed)
            batch_payloads.append(payload)
            if payload["Routing Path"] == "EXPRESS_BYPASS":
                express_count += 1
                
        # Append data to rendering history buffer
        history_buffer.extend(batch_payloads)
        if len(history_buffer) > 50:
            history_buffer = history_buffer[-50:]
            
        # Calculate real-time throughput metrics
        end_frame_time = time.time()
        frame_duration = end_frame_time - start_frame_time
        calculated_tps = int(len(raw_batch) / (frame_duration + 0.05)) # avoid division zero
        
        # Convert buffer to DataFrame for Streamlit visual API consumption
        df = pd.DataFrame(history_buffer)
        
        # --- UPDATE UI ELEMENTS LIVE ---
        tps_metric.metric(label="⚡ Current Throughput", value=f"{calculated_tps} TPS", delta="Signals / Sec")
        total_metric.metric(label="📊 Total Signals Processed", value=f"{total_processed:,}")
        active_route_metric.metric(label="🧠 Active Express Bypass", value=f"{express_count} in current batch")
        
        # Update live chart
        if not df.empty:
            chart_placeholder.line_chart(df.set_index("Signal ID")["Voltage (mV)"])
            table_placeholder.dataframe(df.tail(8)[["Signal ID", "Input", "Voltage (mV)", "Routing Path"]], hide_index=True, use_container_width=True)
            
        # Small intentional yield interval to keep the web application fluid and highly responsive
        time.sleep(0.05)
else:
    st.info("💡 Turn on 'Start Live Stream' in the left control panel to begin streaming high-frequency data.")
