
# 📦 API Clients – MSPR_4

Microservice de gestion des **clients** pour le projet MSPR Bloc 4, développé avec **FastAPI**, **MongoDB**, **RabbitMQ** et sécurisé via **JWT**. Ce microservice est conçu pour fonctionner dans une architecture **microservices** et s’intègre via un repo principal avec `docker-compose`.

---

## Fonctionnalités

- Création, lecture, mise à jour et suppression de clients
- Connexion à MongoDB
- Sécurité JWT avec rôles (`admin`, `user`)
- Communication asynchrone via RabbitMQ
- Monitoring Prometheus (exposé sur `/metrics`)
- Analyse de qualité via SonarCloud
- Couverture de tests avec `pytest`

---

## Structure du projet

```bash
app/
├── db/                # Connexion MongoDB
├── models/            # Modèle Client (Pydantic + ObjectId compatible)
├── routes/            # Endpoints REST (clients, token)
├── services/          # Logique métier (CRUD MongoDB)
├── messaging/         # RabbitMQ : publisher & consumer
├── security/          # JWT, dépendances de sécurité
├── utils/             # (réservé pour helpers futurs)
├── config.py          # Chargement de l'environnement
└── main.py            # Entrée principale FastAPI
```

---

## Authentification JWT

L’API utilise des **tokens JWT** avec rôles pour sécuriser les routes :

- Endpoint de login : `POST /token`
- En-tête requis : `Authorization: Bearer <token>`

> Les rôles gérés sont :  
> `admin` → accès complet aux endpoints `/clients`  
> `user` → accès restreint

---

## Monitoring

- Prometheus est intégré via `prometheus_fastapi_instrumentator`
- Les métriques sont accessibles à :  
  `GET /metrics`

---

## Endpoints principaux

| Méthode | Endpoint            | Sécurité           | Description                 |
|---------|---------------------|--------------------|-----------------------------|
| POST    | `/token`            |  Public          | Obtenir un token JWT        |
| GET     | `/clients/`         |  admin uniquement | Lister tous les clients     |
| POST    | `/clients/`         |  admin uniquement | Créer un nouveau client     |
| GET     | `/clients/{id}`     |  connecté         | Récupérer un client par ID  |
| PUT     | `/clients/{id}`     |  admin uniquement | Mettre à jour un client     |
| DELETE  | `/clients/{id}`     |  admin uniquement | Supprimer un client         |

---

## Tests

Lancer les tests avec couverture :
```bash
pytest --cov=app --cov-report=term-missing
```

 Couverture actuelle : ~95%  
 Les tests couvrent :
- Endpoints REST
- Authentification JWT
- RabbitMQ (mocké)
- Monitoring `/metrics`

---

## Docker

Un `Dockerfile` est inclus pour builder le microservice :
```bash
docker build -t api-clients .
docker run -p 8000:8000 api-clients
```

> MongoDB et RabbitMQ doivent être accessibles (ou gérés via `docker-compose` dans le repo principal)

---

## .env example

Un fichier `.env.example` est fourni :
```env
APP_NAME=Clients API
MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=clients_db
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256
RABBITMQ_URL=amqp://guest:guest@localhost/
```

---

## Technologies utilisées

- **FastAPI** (Python 3.13)
- **MongoDB**
- **RabbitMQ**
- **JWT (jose)**
- **Pytest + Coverage**
- **Prometheus**
- **Docker**
- **SonarCloud**

---

## À faire dans le repo principal

Ce microservice est conçu pour être utilisé comme **submodule Git** dans un repo principal (`MSPR_4`) qui centralise :
- Les 3 microservices (`clients`, `produits`, `commandes`)
- La stack `docker-compose`
- Prometheus + Grafana