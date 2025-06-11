from fastapi import HTTPException
from app.security.dependencies import get_current_user, role_required
import pytest

def test_get_current_user_valid():
    from app.security.auth import create_access_token
    token = create_access_token({"sub": "user", "role": "user"})
    payload = get_current_user(token)
    assert payload["sub"] == "user"

def test_get_current_user_invalid():
    with pytest.raises(HTTPException) as exc:
        get_current_user("invalid.token")
    assert exc.value.status_code == 401

def test_role_required_valid():
    checker = role_required("admin")
    user = {"sub": "admin", "role": "admin"}
    assert checker(user) == user

def test_role_required_invalid():
    checker = role_required("admin")
    with pytest.raises(HTTPException) as exc:
        checker({"sub": "user", "role": "user"})
    assert exc.value.status_code == 403
