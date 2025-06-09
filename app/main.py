"""Point d'entrée principal de l'API Clients avec monitoring Prometheus."""

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from app.routes import clients, token  # 🔹 Ajout du router 'token'

app = FastAPI(
    title="Clients API",
    version="1.0.0",
    description="API de gestion des clients pour PayeTonKawa"
)

# Monitoring Prometheus
Instrumentator().instrument(app).expose(app)

@app.get("/")
def root():
    """Affiche un message de bienvenue."""
    return {"msg": "Bienvenue sur l'API Clients"}

# Inclusions des routes
app.include_router(token.router)  # 🔹 Ajout du router /token
app.include_router(clients.router, prefix="/clients", tags=["clients"])
