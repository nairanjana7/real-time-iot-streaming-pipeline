from fastapi import APIRouter, Depends

from backend.dependencies.auth import get_current_user
from backend.models.user import User

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"],
)


@router.get("/me")
def current_user(
    user: User = Depends(get_current_user),
):

    return {
        "id": user.id,
        "company_id": user.company_id,
        "name": user.full_name,
        "email": user.email,
        "role": user.role,
    }
