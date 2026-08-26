from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

app = FastAPI(
    title="3D Medical Spatial Twin - HPC Telemetry API",
    version="1.0.0",
    description="Microservice backend for cardio-neural spatial telemetry and node processing."
)

# Pydantic model for incoming telemetry configuration
class SimulationConfig(BaseModel):
    node_count: int = 500

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "HPC Telemetry & Spatial Twin Core",
        "location": "Doha, Qatar"
    }

@app.post("/api/v1/telemetry/generate")
def generate_telemetry(config: SimulationConfig):
    # Simulate high-performance spatial nodes coordinate generation
    coords = np.random.uniform(-50.0, 50.0, (config.node_count, 3)).tolist()
    
    # Calculate dispersion metrics
    arr = np.array(coords)
    diff = arr[:, np.newaxis, :] - arr[np.newaxis, :, :]
    max_dispersion = float(np.max(np.linalg.norm(diff, axis=-1)))
    
    return {
        "active_nodes": config.node_count,
        "max_spatial_dispersion_mm": round(max_dispersion, 2),
        "coordinates_sample": coords[:5] # Returning first 5 sample nodes
    }