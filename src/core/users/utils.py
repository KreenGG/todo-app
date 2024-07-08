import hashlib
from datetime import datetime, timedelta, timezone

import jwt

from src.config import settings


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed_password: str) -> bool:
    return hash_password(password) == hashed_password


def create_access_token(data: dict):
    to_encode = data.copy()
    expire_at = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt.expires_minutes)
    to_encode.update({"exp": expire_at})
    token = jwt.encode(to_encode, settings.jwt.secret, algorithm="HS256")

    return token
