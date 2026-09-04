from datetime import datetime

from pydantic import BaseModel


class TelemetryCreate(BaseModel):
    machine_id: int

    voltage: float
    current: float
    heat: float

    temperature: float
    pressure: float
    humidity: float
    vibration: float
    rpm: int


class TelemetryResponse(BaseModel):
    machine_id: int

    voltage: float
    current: float
    heat: float

    temperature: float
    pressure: float
    humidity: float
    vibration: float
    rpm: int

    timestamp: datetime
