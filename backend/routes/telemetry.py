from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/telemetry",
    tags=["Telemetry"]
)


@router.get("/health")
def telemetry_health():
    return {
        "module": "Telemetry",
        "status": "Running"
    }
