from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from backend.routes.auth import router as auth_router
from backend.routes.user import router as user_router
from backend.routes.machines import router as machine_router
from backend.routes.prediction import router as prediction_router
from backend.routes.telemetry import router as telemetry_router

app = FastAPI(
    title="PredictGuard AI Platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(prediction_router)
app.include_router(machine_router)
app.include_router(telemetry_router)


@app.get("/")
def root():
    return {
        "message": "PredictGuard AI Backend Running"
    }
