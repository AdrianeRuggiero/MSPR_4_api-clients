from typing import List, Optional
from app.models.client import ClientModel, PyObjectId
from app.db.mongo import clients_collection
from bson import ObjectId

# Créer un nouveau client
def create_client(client: ClientModel) -> ClientModel:
    client_dict = client.dict(by_alias=True, exclude_unset=True)
    result = clients_collection.insert_one(client_dict)
    client_dict["_id"] = result.inserted_id
    return ClientModel(**client_dict)

# Obtenir un client par ID
def get_client(client_id: str) -> Optional[ClientModel]:
    if not ObjectId.is_valid(client_id):
        return None
    client_data = clients_collection.find_one({"_id": ObjectId(client_id)})
    return ClientModel(**client_data) if client_data else None

# Lister tous les clients
def list_clients() -> List[ClientModel]:
    return [ClientModel(**doc) for doc in clients_collection.find()]

# Mettre à jour un client
def update_client(client_id: str, client: ClientModel) -> Optional[ClientModel]:
    if not ObjectId.is_valid(client_id):
        return None
    updated = clients_collection.find_one_and_update(
        {"_id": ObjectId(client_id)},
        {"$set": client.dict(by_alias=True, exclude_unset=True)},
        return_document=True
    )
    return ClientModel(**updated) if updated else None

# Supprimer un client
def delete_client(client_id: str) -> bool:
    if not ObjectId.is_valid(client_id):
        return False
    result = clients_collection.delete_one({"_id": ObjectId(client_id)})
    return result.deleted_count == 1
