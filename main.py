from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI(title="HPC Telemetry & Spatial Twin Core")

# হোম রুট (যা আপনি ইতিমধ্যেই দেখছেন)
@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "HPC Telemetry & Spatial Twin Core",
        "location": "Doha, Qatar"
    }

# ১. টেলিমেট্রি ডেটা পাওয়ার রুট (HPC Telemetry Data)
@app.get("/api/telemetry")
def get_telemetry():
    return {
        "cpu_usage_pct": 42.5,
        "gpu_memory_mb": 8192,
        "latency_ms": 12,
        "status": "HEALTHY"
    }

# ২. স্পেশাল টুইন টপোলজি ডেটা সাবমিট করার জন্য স্কিমা ও রুট (POST Request)
class SpatialPoint(BaseModel):
    point_id: str
    x: float
    y: float
    z: float
    metadata: Dict[str, str]

@app.post("/api/topology/update")
def update_topology(point: SpatialPoint):
    # এখানে আপনি medical_topology.py এর লজিক কল করতে পারেন
    return {
        "message": f"Point {point.point_id} successfully updated in spatial twin map.",
        "received_coordinates": {"x": point.x, "y": point.y, "z": point.z}
    }
