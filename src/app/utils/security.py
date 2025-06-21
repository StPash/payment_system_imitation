import jwt
import hashlib
from datetime import datetime, timedelta

from fastapi import HTTPException

from src.app.config import settings


def get_access_token(user_id: int) -> str:
    expires = datetime.utcnow() + timedelta(minutes=5)
    return jwt.encode(
        {"sub": str(user_id), "exp": expires},
        settings.SECRET_KEY,
        algorithm="HS256"
    )


def get_refresh_token(user_id: int) -> str:
    expires = datetime.utcnow() + timedelta(minutes=10)
    return jwt.encode(
        {"sub": str(user_id), "exp": expires},
        settings.SECRET_KEY_REFRESH,
        algorithm="HS256"
    )


def decode_access_token(access_token: str) -> int:
    try:
        payload = jwt.decode(jwt=access_token, key=settings.SECRET_KEY, algorithms=["HS256"])
        return int(payload['sub'])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Access token истек")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Невалидный access token")


def decode_refresh_token(refresh_token: str) -> int:
    try:
        payload = jwt.decode(
            jwt=refresh_token,
            key=settings.SECRET_KEY_REFRESH,
            algorithms=["HS256"]
        )
        return int(payload['sub'])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token истек")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Невалидный refresh token")


def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password_hash, password):
    return password_hash == hashlib.sha256(password.encode()).hexdigest()
