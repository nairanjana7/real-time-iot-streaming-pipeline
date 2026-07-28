from fastapi import APIRouter

from backend.services.system_service import get_system_health


router = APIRouter(

    prefix="/api/v1/system",

    tags=["System"]

)


@router.get("/health")

def system_health():

    return get_system_health()
