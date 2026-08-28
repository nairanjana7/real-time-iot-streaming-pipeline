from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.database import get_db

from backend.schemas.auth import (
    CompanyRegisterRequest,
    LoginRequest,
    TokenResponse,
)

from backend.services.auth_service import AuthService

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)


@router.post("/register-company")
def register_company(
    request: CompanyRegisterRequest,
    db: Session = Depends(get_db),
):
    try:
        return AuthService.register_company(
            request=request,
            db=db,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    try:
        return AuthService.login(
            request=request,
            db=db,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
        )
