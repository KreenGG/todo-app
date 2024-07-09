from abc import ABC, abstractmethod
from typing import Annotated

from fastapi import Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_session_stub
from src.core.users.entities import User
from src.core.users.models import UserModel
from src.core.users.schemas import UserRegisterSchema


class BaseUserRepository(ABC):
    @abstractmethod
    def find_by_id(self, user_id: int) -> User:
        ...

    @abstractmethod
    def find_by_email(self, email: str) -> User:
        ...

    @abstractmethod
    def add(self, user: UserRegisterSchema) -> User:
        ...


class SQLAlchemyUserRepository(BaseUserRepository):
    def __init__(self, session: Annotated[AsyncSession, Depends(get_session_stub)]) -> None:
        self.session = session

    async def find_by_id(self, user_id: int) -> User:
        query = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(query)
        result = result.scalar_one_or_none()
        if not result:
            return None
        return result.to_entity()

    async def find_by_email(self, email: str) -> User:
        query = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(query)
        result = result.scalar_one_or_none()
        if not result:
            return None
        return result.to_entity()

    async def add(self, email: str, hashed_password: str) -> User:
        query = insert(UserModel).values(email=email, hashed_password=hashed_password).returning(UserModel)
        result = await self.session.execute(query)
        await self.session.commit()
        return result.scalar_one().to_entity()
