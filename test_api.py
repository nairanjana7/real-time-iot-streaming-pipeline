from fastapi.testclient import TestClient
from unittest.mock import patch

from backend.main import app

client = TestClient(app)


VALID_TELEMETRY = {
    "machine_id": 2,
    "temperature": 25.5,
    "pressure": 1.2,
    "humidity": 60.0,
    "vibration": 0.15,
    "rpm": 1500,
}


def test_telemetry_requires_auth():
    response = client.post(
        "/api/v1/telemetry/",
        json=VALID_TELEMETRY,
    )

    assert response.status_code == 401


def test_invalid_telemetry_requires_auth():
    invalid_payload = {
        "machine_id": 2,
        "temperature": "not-a-number",
    }

    response = client.post(
        "/api/v1/telemetry/",
        json=invalid_payload,
    )

    assert response.status_code == 401


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "PredictGuard AI Backend Running"
    }


def test_protected_latest_requires_auth():
    response = client.get("/api/v1/telemetry/latest/2")

    assert response.status_code == 401
