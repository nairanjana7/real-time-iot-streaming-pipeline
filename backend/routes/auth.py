from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)


@router.get("/health")
def auth_health():
    return {
        "module": "Authentication",
        "status": "Running"
    }
