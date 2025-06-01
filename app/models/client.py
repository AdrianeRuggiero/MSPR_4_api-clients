from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from bson import ObjectId

# Pydantic ne supporte pas ObjectId nativement, donc on crée un champ custom
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

# Modèle stocké dans MongoDB
class ClientModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    name: str
    email: EmailStr
    company: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool = True

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jean Dupont",
                "email": "jean.dupont@entreprise.fr",
                "company": "Café du Coin",
                "phone": "+33123456789",
                "is_active": True
            }
        }
