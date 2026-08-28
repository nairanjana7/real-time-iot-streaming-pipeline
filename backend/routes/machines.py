from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.dependencies.auth import get_current_user

from backend.models.user import User

from backend.schemas.machine import (
    MachineCreate,
    MachineUpdate,
    MachineResponse,
)

from backend.services.machine_service import (
    MachineService,
)

router = APIRouter(
    prefix="/api/v1/machines",
    tags=["Machines"],
)


@router.post(
    "/",
    response_model=MachineResponse,
)
def create_machine(
    request: MachineCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):

    try:

        return MachineService.create_machine(
            db,
            user,
            request,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "/",
    response_model=list[MachineResponse],
)
def get_all(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):

    return MachineService.get_all(
        db,
        user,
    )


@router.get(
    "/{machine_id}",
    response_model=MachineResponse,
)
def get_machine(
    machine_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):

    try:

        return MachineService.get_by_id(
            db,
            user,
            machine_id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.put(
    "/{machine_id}",
    response_model=MachineResponse,
)
def update_machine(
    machine_id: int,
    request: MachineUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):

    try:

        return MachineService.update_machine(
            db,
            user,
            machine_id,
            request,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.delete("/{machine_id}")
def delete_machine(
    machine_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):

    try:

        return MachineService.delete_machine(
            db,
            user,
            machine_id,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
