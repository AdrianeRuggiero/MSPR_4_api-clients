from pydantic import BaseModel, EmailStr
from typing import Optional

class ClientBaseMessage(BaseModel):
    name: str
    email: EmailStr
    company: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool

class ClientCreatedMessage(ClientBaseMessage):
    pass

class ClientUpdatedMessage(ClientBaseMessage):
    _id: str

class ClientDeletedMessage(BaseModel):
    _id: str
