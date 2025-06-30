from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.models.client import ClientModel
from app.services.client_service import (
    create_client, get_client, list_clients, update_client, delete_client
)
from app.security.dependencies import get_current_user, role_required
from app.messaging.rabbitmq import (
    publish_client_created, publish_client_updated, publish_client_deleted
)

router = APIRouter()

@router.post("/", response_model=ClientModel, status_code=status.HTTP_201_CREATED)
def create(client: ClientModel, user=Depends(role_required("admin"))):
    new_client = create_client(client)
    publish_client_created(new_client.dict())
    return new_client

@router.get("/", response_model=List[ClientModel], dependencies=[Depends(role_required("admin"))])
def get_all(user=Depends(get_current_user)):
    return list_clients()

@router.get("/{client_id}", response_model=ClientModel)
def get_by_id(client_id: str, user=Depends(get_current_user)):
    client = get_client(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    return client

@router.put("/{client_id}", response_model=ClientModel)
def update(client_id: str, client: ClientModel, user=Depends(role_required("admin"))):
    updated = update_client(client_id, client)
    if not updated:
        raise HTTPException(status_code=404, detail="Client non trouvé ou non modifié")
    publish_client_updated(updated.dict())
    return updated

@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(client_id: str, user=Depends(role_required("admin"))):
    success = delete_client(client_id)
    if not success:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    publish_client_deleted(client_id)
    return
