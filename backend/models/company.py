from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from backend.database.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False)

    industry = Column(String(100))

    email = Column(String(150), unique=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    users = relationship(
        "User",
        back_populates="company",
        cascade="all, delete-orphan"
    )

    machines = relationship(
        "Machine",
        back_populates="company",
        cascade="all, delete-orphan"
    )
