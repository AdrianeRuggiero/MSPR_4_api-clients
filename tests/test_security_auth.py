from app.security.auth import verify_token

def test_verify_token_valid():
    from app.security.auth import create_access_token
    token = create_access_token({"sub": "test", "role": "admin"})
    decoded = verify_token(token)
    assert decoded["sub"] == "test"
    assert decoded["role"] == "admin"

def test_verify_token_invalid():
    assert verify_token("invalid.token.here") is None
