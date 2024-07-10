import hashlib
from datetime import datetime, timedelta, timezone
from time import time

from fastapi import Request
import jwt

from .exceptions import TokenAbsentException, TokenExpiredException
from src.config import settings


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed_password: str) -> bool:
    return hash_password(password) == hashed_password


def create_access_token(data: dict):
    to_encode = data.copy()
    expire_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.jwt.expires_minutes
    )
    to_encode.update({"exp": expire_at})
    token = jwt.encode(to_encode, settings.jwt.secret, algorithm=settings.jwt.algorithm)

    return token


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise TokenAbsentException
    return token


# TODO: МБ снять асинк с методов


def get_token_payload(token: bytes) -> dict:
    payload = jwt.decode(
        token, settings.jwt.secret, algorithms=[settings.jwt.algorithm]
    )

    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < time()):
        raise TokenExpiredException

    return payload
