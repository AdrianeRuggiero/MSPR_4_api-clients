from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from app.routes import clients

app = FastAPI(
    title="Clients API",
    version="1.0.0",
    description="API de gestion des clients pour PayeTonKawa"
)

# Monitoring Prometheus
Instrumentator().instrument(app).expose(app)

# Route racine
@app.get("/")
def root():
    return {"msg": "Bienvenue sur l'API Clients"}

# Inclusions des routes clients
app.include_router(clients.router, prefix="/clients", tags=["clients"])
