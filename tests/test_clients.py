from fastapi.testclient import TestClient
from app.main import app
from app.security.auth import create_access_token

client = TestClient(app)

def get_auth_headers(role="admin"):
    token = create_access_token({"sub": "testuser", "role": role})
    return {"Authorization": f"Bearer {token}"}

def test_create_client():
    payload = {
        "name": "Test Client",
        "email": "test@example.com",
        "company": "TestCorp",
        "phone": "+330000000",
        "is_active": True
    }
    response = client.post("/clients/", json=payload, headers=get_auth_headers())
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Client"

def test_list_clients():
    response = client.get("/clients/", headers=get_auth_headers())
    assert response.status_code == 200
    assert isinstance(response.json(), list)
