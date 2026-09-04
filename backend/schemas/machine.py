from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MachineCreate(BaseModel):
    machine_name: str
    serial_number: str
    machine_type: Optional[str] = None
    location: Optional[str] = None


class MachineUpdate(BaseModel):
    machine_name: Optional[str] = None
    machine_type: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None


class MachineResponse(BaseModel):
    id: int
    company_id: int
    machine_name: str
    serial_number: str
    machine_type: Optional[str]
    location: Optional[str]
    status: str
    device_api_key: Optional[str]
    installed_at: datetime

    class Config:
        from_attributes = True
