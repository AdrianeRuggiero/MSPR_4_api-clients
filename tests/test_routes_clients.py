from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.security.auth import create_access_token

client = TestClient(app)

def get_auth_headers(role="admin"):
    token = create_access_token({"sub": "testuser", "role": role})
    return {"Authorization": f"Bearer {token}"}

@patch("app.routes.clients.publish_client_created")
def test_create_client(mock_publish):
    payload = {
        "name": "Test Client",
        "email": "test@example.com",
        "company": "TestCorp",
        "phone": "+330000000",
        "is_active": True
    }
    response = client.post("/clients/", json=payload, headers=get_auth_headers())
    assert response.status_code == 201
    assert response.json()["name"] == "Test Client"

@patch("app.routes.clients.publish_client_updated")
@patch("app.routes.clients.publish_client_created")
def test_update_client(mock_created, mock_updated):
    payload = {
        "name": "Old Name",
        "email": "update@example.com",
        "company": "OldCorp",
        "phone": "+33123456789",
        "is_active": True
    }
    create_resp = client.post("/clients/", json=payload, headers=get_auth_headers())
    client_id = create_resp.json()["_id"]

    updated = {
        "name": "New Name",
        "email": "update@example.com",
        "company": "NewCorp",
        "phone": "+33999999999",
        "is_active": False
    }
    response = client.put(f"/clients/{client_id}", json=updated, headers=get_auth_headers())
    assert response.status_code == 200

@patch("app.routes.clients.publish_client_deleted")
@patch("app.routes.clients.publish_client_created")
def test_delete_client(mock_created, mock_deleted):
    payload = {"name": "Delete Me", "email": "delete@example.com"}
    create_resp = client.post("/clients/", json=payload, headers=get_auth_headers())
    client_id = create_resp.json()["_id"]

    delete_resp = client.delete(f"/clients/{client_id}", headers=get_auth_headers())
    assert delete_resp.status_code == 204

    get_resp = client.get(f"/clients/{client_id}", headers=get_auth_headers())
    assert get_resp.status_code == 404

def test_list_clients():
    response = client.get("/clients/", headers=get_auth_headers())
    assert response.status_code == 200

@patch("app.routes.clients.publish_client_created")
def test_get_single_client(mock_created):
    payload = {"name": "Client X", "email": "clientx@example.com"}
    create_resp = client.post("/clients/", json=payload, headers=get_auth_headers())
    client_id = create_resp.json()["_id"]

    get_resp = client.get(f"/clients/{client_id}", headers=get_auth_headers())
    assert get_resp.status_code == 200

@patch("app.routes.clients.publish_client_updated")
@patch("app.routes.clients.publish_client_created")
def test_update_client_no_change(mock_updated, mock_created):
    payload = {"name": "SameName", "email": "same@example.com"}
    create_resp = client.post("/clients/", json=payload, headers=get_auth_headers())
    client_id = create_resp.json()["_id"]

    response = client.put(f"/clients/{client_id}", json=payload, headers=get_auth_headers())
    assert response.status_code == 200
