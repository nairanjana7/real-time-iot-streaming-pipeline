from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from backend.core.config import settings
from backend.database.database import get_db
from backend.models.user import User

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    print("\n========== AUTH DEBUG ==========")
    print("TOKEN:", token)
    print("SECRET:", settings.SECRET_KEY)
    print("ALGORITHM:", settings.ALGORITHM)

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        print("PAYLOAD:", payload)
        print("===============================\n")

        email = payload.get("sub")

        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing subject in token",
            )

    except JWTError as e:
        print("JWT ERROR:", repr(e))

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user
from backend.models.machine import Machine


def get_current_machine(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    api_key = credentials.credentials

    machine = (
        db.query(Machine)
        .filter(Machine.device_api_key == api_key)
        .first()
    )

    if machine is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid device API key",
        )

    return machine

from backend.models.machine import Machine


def get_current_machine(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    """
    Authenticate an IoT device using its machine-specific API key.

    The API key determines which machine is sending the telemetry.
    The client does not get to choose the machine_id.
    """

    device_api_key = credentials.credentials

    machine = (
        db.query(Machine)
        .filter(
            Machine.device_api_key == device_api_key
        )
        .first()
    )

    if machine is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid device API key",
        )

    return machine
