from abc import ABC, abstractmethod

from dishka import FromDishka
from fastapi import Request

from .entities import User
from .exceptions import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from .repository import BaseUserRepository
from .schemas import UserLoginSchema, UserRegisterSchema
from .utils import (
    create_access_token,
    get_token,
    get_token_payload,
    hash_password,
    verify_password,
)


class BaseUserService(ABC):
    @abstractmethod
    def register_user(self, user: UserRegisterSchema) -> User:
        ...

    @abstractmethod
    def login_user(self, user: UserLoginSchema) -> int:
        ...

    @abstractmethod
    def get_current_user(self, token: str) -> User:
        ...


class ORMUserService:
    def __init__(self, repo: FromDishka[BaseUserRepository]) -> None:
        self.repo = repo

    async def register_user(self, user: UserRegisterSchema) -> User:
        if await self.repo.find_by_email(user.email):
            raise UserAlreadyExistsException
        hashed_password = hash_password(user.password)
        created_user = await self.repo.add(user.email, hashed_password)

        return created_user

    async def login_user(self, user: UserLoginSchema) -> int:
        user_db = await self.repo.find_by_email(user.email)
        if not user_db:
            raise UserNotFoundException

        if not verify_password(user.password, user_db.hashed_password):
            raise InvalidCredentialsException

        token = create_access_token(data={"sub": user_db.id})
        return token

    async def get_current_user(self, request: Request) -> User:
        token = get_token(request)
        payload = get_token_payload(token)
        user_id = payload.get("sub")
        user = await self.repo.find_by_id(user_id)
        return user
