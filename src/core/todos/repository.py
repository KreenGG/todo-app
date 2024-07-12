from abc import ABC, abstractmethod
from typing import Iterable

from dishka.integrations.fastapi import FromDishka
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.users.entities import User

from .entities import Todo
from .models import TodoModel
from .schemas import TodoAddSchema


class BaseTodoRepository(ABC):
    @abstractmethod
    async def find_all(self, user: User) -> Iterable[Todo]:
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, user: User, todo_id: int) -> Todo:
        raise NotImplementedError

    @abstractmethod
    async def add(self, user: User, todo: TodoAddSchema) -> Todo:
        raise NotImplementedError

    @abstractmethod
    async def update(self, user: User, todo: dict, todo_id: int) -> Todo:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, user: User, todo_id: int) -> None:
        raise NotImplementedError


class SQLAlchemyTodoRepository(BaseTodoRepository):
    def __init__(self, session: FromDishka[AsyncSession]) -> None:
        self.session: AsyncSession = session

    async def find_all(
        self,
        user: User,
    ) -> Iterable[Todo]:
        query = (
            select(TodoModel)
            .where(TodoModel.user_id == user.id)
            .order_by(TodoModel.created_at)
        )
        result = await self.session.execute(query)
        result_orm = result.scalars().all()

        todo_list = [row.to_entity() for row in result_orm]
        return todo_list

    async def find_by_id(self, user: User, todo_id: int) -> Todo:
        query = select(TodoModel).where(
            TodoModel.id == todo_id and TodoModel.user_id == user.id
        )
        result = await self.session.execute(query)
        result_orm = result.scalars().first()

        if not result_orm:
            return None
        todo = result_orm.to_entity()
        return todo

    async def add(self, user: User, todo: TodoAddSchema) -> Todo:
        query = (
            insert(TodoModel)
            .values(**todo.__dict__, user_id=user.id)
            .returning(TodoModel)
        )
        result = await self.session.execute(query)
        await self.session.commit()
        return result.scalar_one().to_entity()

    async def update(self, user: User, todo: dict, todo_id: int) -> Todo:
        query = (
            update(TodoModel)
            .where(TodoModel.id == todo_id, TodoModel.user_id == user.id)
            .values(**todo)
            .returning(TodoModel)
        )
        result = await self.session.execute(query)
        await self.session.commit()
        return result.scalar_one().to_entity()

    async def delete(self, user: User, todo_id: int) -> None:
        query = delete(TodoModel).where(
            TodoModel.id == todo_id and TodoModel.user_id == user.id
        )
        await self.session.execute(query)
        await self.session.commit()
