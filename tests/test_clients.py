from fastapi.testclient import TestClient
from bson import ObjectId
from datetime import timedelta
from jose import jwt, JWTError
import time
from unittest.mock import patch

from app.main import app
from app.models.client import ClientModel
from app.security.auth import create_access_token, verify_token
from app.services.client_service import (
    create_client, get_client, list_clients, update_client, delete_client
)
from app.messaging.rabbitmq import publish_client_created

client = TestClient(app)

def get_auth_headers(role="admin"):
    token = create_access_token({"sub": "testuser", "role": role})
    return {"Authorization": f"Bearer {token}"}

# ROUTES

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
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]

def test_list_clients():
    response = client.get("/clients/", headers=get_auth_headers())
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_single_client():
    payload = {
        "name": "Client X",
        "email": "clientx@example.com"
    }
    create_resp = client.post("/clients/", json=payload, headers=get_auth_headers())
    client_id = create_resp.json()["_id"]

    get_resp = client.get(f"/clients/{client_id}", headers=get_auth_headers())
    assert get_resp.status_code == 200
    assert get_resp.json()["email"] == "clientx@example.com"

def test_get_not_found():
    fake_id = str(ObjectId())
    response = client.get(f"/clients/{fake_id}", headers=get_auth_headers())
    assert response.status_code == 404

def test_update_client():
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
    update_resp = client.put(f"/clients/{client_id}", json=updated, headers=get_auth_headers())
    assert update_resp.status_code == 200
    assert update_resp.json()["name"] == "New Name"

def test_update_not_found():
    fake_id = str(ObjectId())
    updated_data = {"name": "DoesNotExist", "email": "fake@email.com"}
    resp = client.put(f"/clients/{fake_id}", json=updated_data, headers=get_auth_headers())
    assert resp.status_code == 404

def test_delete_client():
    payload = {"name": "Delete Me", "email": "delete@example.com"}
    create_resp = client.post("/clients/", json=payload, headers=get_auth_headers())
    client_id = create_resp.json()["_id"]

    delete_resp = client.delete(f"/clients/{client_id}", headers=get_auth_headers())
    assert delete_resp.status_code == 204

    get_resp = client.get(f"/clients/{client_id}", headers=get_auth_headers())
    assert get_resp.status_code == 404

def test_delete_not_found():
    fake_id = str(ObjectId())
    response = client.delete(f"/clients/{fake_id}", headers=get_auth_headers())
    assert response.status_code == 404

def test_unauthorized_access():
    response = client.get("/clients/")
    assert response.status_code == 401

def test_forbidden_role():
    token = create_access_token({"sub": "user", "role": "user"})
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/clients/", headers=headers)
    assert response.status_code == 403

# SERVICES

def test_get_client_direct():
    payload = {
        "name": "FromService",
        "email": "service@example.com",
        "company": "ServCorp",
        "phone": "+33777777777",
        "is_active": True
    }
    resp = client.post("/clients/", json=payload, headers=get_auth_headers())
    client_id = resp.json()["_id"]

    result = get_client(client_id)
    assert result is not None
    assert result.name == "FromService"

def test_update_client_no_change():
    payload = {"name": "SameName", "email": "same@example.com"}
    create_resp = client.post("/clients/", json=payload, headers=get_auth_headers())
    client_id = create_resp.json()["_id"]

    updated_data = {"name": "SameName", "email": "same@example.com"}
    update_resp = client.put(f"/clients/{client_id}", json=updated_data, headers=get_auth_headers())
    assert update_resp.status_code == 200

def test_update_client_invalid_id():
    updated_data = {"name": "Updated", "email": "up@example.com"}
    resp = client.put("/clients/not-a-valid-id", json=updated_data, headers=get_auth_headers())
    assert resp.status_code == 404

def test_delete_client_invalid_id():
    resp = client.delete("/clients/invalid-id", headers=get_auth_headers())
    assert resp.status_code == 404

# AUTH

def test_token_expiration():
    short_token = create_access_token(data={"sub": "user"}, expires_delta=timedelta(seconds=1))
    time.sleep(2)
    result = verify_token(short_token)
    assert result is None

def test_verify_valid_token():
    token = create_access_token({"sub": "user"})
    decoded = verify_token(token)
    assert decoded["sub"] == "user"

# MESSAGING

def test_publish_client_created():
    sample_data = {"_id": "123", "name": "Test"}
    with patch("app.messaging.rabbitmq.channel.basic_publish") as mock_pub:
        publish_client_created(sample_data)
        mock_pub.assert_called_once()
