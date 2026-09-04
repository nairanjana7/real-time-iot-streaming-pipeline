from fastapi.testclient import TestClient

from backend.main import app
from backend.services.telemetry_service import TelemetryService
from backend.core.security import create_access_token
from backend.database.database import SessionLocal
from backend.models.machine import Machine

client = TestClient(app)


VALID_TELEMETRY = {
    "machine_id": 4,
    "voltage": 230.0,
    "current": 5.2,
    "heat": 72.5,
    "temperature": 35.5,
    "pressure": 993.3,
    "humidity": 36.5,
    "vibration": 3.8,
    "rpm": 1867,
}


def auth_headers():
    """
    Normal authenticated dashboard/user request.
    """
    token = create_access_token(
        {"sub": "admin@predictguard.ai"}
    )

    return {
        "Authorization": f"Bearer {token}"
    }


def device_auth_headers():
    """
    Authentication for machine telemetry ingestion.

    Retrieves a real registered machine API key from the database.
    """

    db = SessionLocal()

    try:
        machine = (
            db.query(Machine)
            .filter(
                Machine.serial_number == "PG-PROVISION-001"
            )
            .first()
        )

        assert machine is not None, (
            "Provisioning test machine does not exist."
        )

        assert machine.device_api_key is not None, (
            "Provisioning test machine has no device API key."
        )

        return {
            "Authorization": f"Bearer {machine.device_api_key}"
        }

    finally:
        db.close()


def test_telemetry_valid_payload_returns_200(monkeypatch):

   def fake_write(request, machine_id):
    return {
        "message": "Telemetry stored successfully."
    }

    monkeypatch.setattr(
        TelemetryService,
        "write",
        fake_write,
    )

    response = client.post(
        "/api/v1/telemetry/",
        json=VALID_TELEMETRY,
        headers=device_auth_headers(),
    )

    assert response.status_code == 200

    assert response.json() == {
        "message": "Telemetry stored successfully."
    }


def test_telemetry_missing_field_returns_422():

    payload = VALID_TELEMETRY.copy()
    del payload["temperature"]

    response = client.post(
        "/api/v1/telemetry/",
        json=payload,
        headers=device_auth_headers(),
    )

    assert response.status_code == 422


def test_telemetry_wrong_type_returns_422():

    payload = VALID_TELEMETRY.copy()
    payload["temperature"] = "not-a-number"

    response = client.post(
        "/api/v1/telemetry/",
        json=payload,
        headers=device_auth_headers(),
    )

    assert response.status_code == 422


def test_telemetry_empty_payload_returns_422():

    response = client.post(
        "/api/v1/telemetry/",
        json={},
        headers=device_auth_headers(),
    )

    assert response.status_code == 422


def test_telemetry_without_auth_returns_401():

    response = client.post(
        "/api/v1/telemetry/",
        json=VALID_TELEMETRY,
    )

    assert response.status_code == 401


def test_protected_latest_without_auth_returns_401():

    response = client.get(
        "/api/v1/telemetry/latest/4"
    )

    assert response.status_code == 401


def test_valid_token_can_access_latest(monkeypatch):

    def fake_latest(machine_id):
        return []

    monkeypatch.setattr(
        TelemetryService,
        "latest",
        fake_latest,
    )

    response = client.get(
        "/api/v1/telemetry/latest/4",
        headers=auth_headers(),
    )

    assert response.status_code == 200
    assert response.json() == []
