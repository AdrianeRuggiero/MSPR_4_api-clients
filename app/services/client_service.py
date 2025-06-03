from typing import List, Optional
from app.models.client import ClientModel, PyObjectId
from app.db.mongo import clients_collection
from bson import ObjectId

# Créer un nouveau client
def create_client(client: ClientModel) -> ClientModel:
    client_dict = client.model_dump(by_alias=True, exclude_unset=True)
    result = clients_collection.insert_one(client_dict)
    client_dict["_id"] = str(result.inserted_id)  # ✅ Corrigé : convertir ObjectId → str
    return ClientModel(**client_dict)

# Obtenir un client par ID
def get_client(client_id: str) -> Optional[ClientModel]:
    if not ObjectId.is_valid(client_id):
        return None
    client_data = clients_collection.find_one({"_id": ObjectId(client_id)})
    if client_data:
        client_data["_id"] = str(client_data["_id"])  # ✅ Corrigé ici aussi
        return ClientModel(**client_data)
    return None

# Lister tous les clients
def list_clients() -> List[ClientModel]:
    clients = []
    for doc in clients_collection.find():
        doc["_id"] = str(doc["_id"])  # ✅ Corrigé pour chaque document
        clients.append(ClientModel(**doc))
    return clients

# Mettre à jour un client
def update_client(client_id: str, client: ClientModel) -> Optional[ClientModel]:
    if not ObjectId.is_valid(client_id):
        return None
    update_data = client.model_dump(by_alias=True, exclude_unset=True)
    updated = clients_collection.find_one_and_update(
        {"_id": ObjectId(client_id)},
        {"$set": update_data},
        return_document=True
    )
    if updated:
        updated["_id"] = str(updated["_id"])  # ✅ Corrigé
        return ClientModel(**updated)
    return None

# Supprimer un client
def delete_client(client_id: str) -> bool:
    if not ObjectId.is_valid(client_id):
        return False
    result = clients_collection.delete_one({"_id": ObjectId(client_id)})
    return result.deleted_count == 1
