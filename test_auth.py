from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_login_rejects_wrong_password():
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "admin@predictguard.ai",
            "password": "definitely-wrong-password",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_login_returns_jwt():
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "admin@predictguard.ai",
            "password": "PredictGuard123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 20


def test_jwt_allows_protected_endpoint():
    login = client.post(
        "/api/v1/auth/login",
        json={
            "email": "admin@predictguard.ai",
            "password": "PredictGuard123",
        },
    )

    assert login.status_code == 200

    token = login.json()["access_token"]

    response = client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "admin@predictguard.ai"
    assert data["company_id"] == 2
    assert data["role"] == "admin"
