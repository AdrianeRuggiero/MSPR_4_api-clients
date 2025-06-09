from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from pydantic_core import core_schema
from pydantic import GetCoreSchemaHandler
from bson import ObjectId


# Compatibilité ObjectId pour Pydantic v2
class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler: GetCoreSchemaHandler):
        return core_schema.no_info_after_validator_function(cls.validate, core_schema.str_schema())

    @classmethod
    def validate(cls, value):
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId")
        return ObjectId(value)


class ClientModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    email: EmailStr
    company: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool = True

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "name": "Jean Dupont",
                "email": "jean.dupont@entreprise.fr",
                "company": "Café du Coin",
                "phone": "+33123456789",
                "is_active": True
            }
        }
