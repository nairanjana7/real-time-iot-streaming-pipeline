from sqlalchemy.orm import Session

from backend.models.machine import Machine


class MachineService:

    @staticmethod
    def create_machine(db: Session, user, request):

        exists = (
            db.query(Machine)
            .filter(
                Machine.serial_number == request.serial_number
            )
            .first()
        )

        if exists:
            raise ValueError(
                "Machine serial already exists."
            )

        machine = Machine(
            company_id=user.company_id,
            machine_name=request.machine_name,
            serial_number=request.serial_number,
            machine_type=request.machine_type,
            location=request.location,
            status="Active",
        )

        db.add(machine)
        db.commit()
        db.refresh(machine)

        return machine

    @staticmethod
    def get_all(db: Session, user):

        return (
            db.query(Machine)
            .filter(
                Machine.company_id == user.company_id
            )
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        user,
        machine_id: int,
    ):

        machine = (
            db.query(Machine)
            .filter(
                Machine.company_id == user.company_id,
                Machine.id == machine_id,
            )
            .first()
        )

        if machine is None:
            raise ValueError(
                "Machine not found."
            )

        return machine

    @staticmethod
    def update_machine(
        db: Session,
        user,
        machine_id,
        request,
    ):

        machine = MachineService.get_by_id(
            db,
            user,
            machine_id,
        )

        data = request.model_dump(
            exclude_unset=True
        )

        for key, value in data.items():
            setattr(machine, key, value)

        db.commit()
        db.refresh(machine)

        return machine

    @staticmethod
    def delete_machine(
        db: Session,
        user,
        machine_id,
    ):

        machine = MachineService.get_by_id(
            db,
            user,
            machine_id,
        )

        db.delete(machine)
        db.commit()

        return {
            "message": "Machine deleted successfully."
        }
