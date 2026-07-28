from fastapi import FastAPI

from backend.routes import auth
from backend.routes import telemetry
from backend.routes import prediction
from backend.routes import system

app = FastAPI(
    title="PredictGuard AI API",
    description="Real-Time Predictive Maintenance Platform",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(telemetry.router)
app.include_router(prediction.router)
app.include_router(system.router)

@app.get("/")
def home():
    return {
        "message": "PredictGuard AI Backend Running"
    }
