from fastapi import APIRouter, Depends

from backend.dependencies.auth import (
    get_current_user,
    get_current_machine,
)

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
    machine=Depends(get_current_machine),
):
    """
    Receive telemetry from an authenticated machine.

    Machine identity comes from the device API key,
    not from the request body.
    """

    return TelemetryService.write(
        request)


@router.get("/latest/{machine_id}")
def latest(
    machine_id: int,
    user=Depends(get_current_user),
):
    return TelemetryService.latest(machine_id)
