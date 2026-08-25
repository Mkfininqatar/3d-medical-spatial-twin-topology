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
