from abc import ABC, abstractmethod
from typing import Annotated

from fastapi import Depends

from src.core.users.entities import User
from src.core.users.exceptions import (InvalidCredentialsException,
                                       UserAlreadyExistsException,
                                       UserNotFoundException)
from src.core.users.repository import BaseUserRepository
from src.core.users.schemas import UserLoginSchema, UserRegisterSchema
from src.core.users.utils import (create_access_token, hash_password,
                                  verify_password)


class BaseUserService(ABC):
    @abstractmethod
    def register_user(self, user: UserRegisterSchema) -> User:
        ...

    @abstractmethod
    def login_user(self, user: UserLoginSchema) -> int:
        ...


class ORMUserService:
    def __init__(
        self,
        repo: Annotated[BaseUserRepository, Depends()],
    ) -> None:
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
