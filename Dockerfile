# Image de base officielle Python
FROM python:3.11-slim

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Dossier de travail
WORKDIR /app

# Copie des fichiers
COPY . .

# Installation des dépendances
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Port exposé
EXPOSE 8000

# Commande de lancement
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
