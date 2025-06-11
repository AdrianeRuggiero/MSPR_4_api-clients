from bson import ObjectId
from app.models.client import ClientModel
from app.services.client_service import create_client, get_client, update_client, delete_client

def test_get_client_direct():
    client_data = ClientModel(name="FromService", email="service@example.com", company="ServCorp", phone="+33777777777", is_active=True)
    result = create_client(client_data)
    assert result.name == "FromService"

def test_get_client_not_found():
    assert get_client(str(ObjectId())) is None

def test_update_client_not_found():
    updated_data = ClientModel(name="DoesNotExist", email="no@email.com")
    assert update_client(str(ObjectId()), updated_data) is None

def test_update_client_invalid_id():
    assert update_client("not-an-id", ClientModel(name="X", email="x@y.com")) is None

def test_delete_client_not_found():
    assert delete_client(str(ObjectId())) is False

def test_delete_client_invalid_id():
    assert delete_client("not-a-valid-id") is False
