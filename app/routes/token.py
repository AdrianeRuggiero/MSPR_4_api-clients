from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.security.auth import create_access_token

router = APIRouter()

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Authentification simplifiée : retourne un JWT avec un rôle
    if form_data.username == "admin":
        role = "admin"
    else:
        role = "user"

    token = create_access_token({"sub": form_data.username, "role": role})
    return {"access_token": token, "token_type": "bearer"}
