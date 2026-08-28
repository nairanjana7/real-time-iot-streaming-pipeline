from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from backend.database.database import Base


class Machine(Base):
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, index=True)

    company_id = Column(
        Integer,
        ForeignKey("companies.id"),
        nullable=False
    )

    machine_name = Column(String(100), nullable=False)

    serial_number = Column(
        String(100),
        unique=True,
        nullable=False
    )

    machine_type = Column(String(100))

    location = Column(String(150))

    status = Column(
        String(30),
        default="Active"
    )

    installed_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    company = relationship(
        "Company",
        back_populates="machines"
    )
