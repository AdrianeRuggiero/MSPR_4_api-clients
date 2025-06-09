"""Configuration du projet FastAPI + MongoDB + JWT + RabbitMQ."""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Paramètres de configuration chargés via un fichier .env."""

    APP_NAME: str = "Clients API"
    MONGO_URI: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "clients_db"
    JWT_SECRET: str = "your-secret-key"
    JWT_ALGORITHM: str = "HS256"
    RABBITMQ_URL: str = "amqp://guest:guest@localhost/"

    class Config:
        """Spécifie le chemin du fichier .env."""
        env_file = ".env"

settings = Settings()

