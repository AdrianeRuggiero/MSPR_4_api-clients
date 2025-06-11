from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_as_admin():
    response = client.post(
        "/token",
        data={"username": "admin", "password": "any"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_as_user():
    response = client.post(
        "/token",
        data={"username": "john", "password": "any"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"