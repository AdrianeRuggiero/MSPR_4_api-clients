from pymongo import MongoClient
from app.config import settings

client = MongoClient(settings.MONGO_URI)
db = client[settings.DATABASE_NAME]

# Exemple d'accès à une collection "clients"
clients_collection = db["clients"]
