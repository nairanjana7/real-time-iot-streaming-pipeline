from fastapi import APIRouter, Depends

from backend.dependencies.auth import get_current_user

from backend.schemas.telemetry import (
    TelemetryCreate,
)

from backend.services.telemetry_service import (
    TelemetryService,
)

router = APIRouter(
    prefix="/api/v1/telemetry",
    tags=["Telemetry"],
)


@router.post("/")
def create(
    request: TelemetryCreate,
    user=Depends(get_current_user),
):

    return TelemetryService.write(request)


@router.get("/latest/{machine_id}")
def latest(
    machine_id: int,
    user=Depends(get_current_user),
):

    return TelemetryService.latest(machine_id)
