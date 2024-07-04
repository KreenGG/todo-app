from abc import ABC, abstractmethod
from typing import Iterable

from fastapi import Depends
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session

from .entities import Todo
from .models import TodoModel
from .schemas import TodoAddSchema


class BaseTodoRepository(ABC):
    @abstractmethod
    async def find_all(self) -> Iterable[Todo]:
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, todo_id: int) -> Todo:
        raise NotImplementedError

    @abstractmethod
    async def add(self, todo: TodoAddSchema) -> Todo:
        raise NotImplementedError

    @abstractmethod
    async def update(self, todo: dict, todo_id: int) -> Todo:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, todo_id: int) -> None:
        raise NotImplementedError


class SQLAlchemyTodoRepository(BaseTodoRepository):
    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        self.session: AsyncSession = session

    async def find_all(self) -> Iterable[Todo]:
        query = select(TodoModel).order_by(TodoModel.created_at)
        result = await self.session.execute(query)
        result_orm = result.scalars().all()

        todo_list = [row.to_entity() for row in result_orm]
        return todo_list

    async def find_by_id(self, todo_id: int) -> Todo:
        query = select(TodoModel).where(TodoModel.id == todo_id)
        result = await self.session.execute(query)
        result_orm = result.scalars().first()

        if not result_orm:
            return None
        todo = result_orm.to_entity()
        return todo

    async def add(self, todo: TodoAddSchema) -> Todo:
        query = insert(TodoModel).values(**todo.__dict__).returning(TodoModel)
        result = await self.session.execute(query)
        await self.session.commit()
        return result.scalar_one().to_entity()

    async def update(self, todo: dict, todo_id: int) -> Todo:
        query = (
            update(TodoModel)
            .where(TodoModel.id == todo_id)
            .values(**todo)
            .returning(TodoModel)
        )
        result = await self.session.execute(query)
        await self.session.commit()
        return result.scalar_one().to_entity()

    async def delete(self, todo_id: int) -> None:
        query = delete(TodoModel).where(TodoModel.id == todo_id)
        await self.session.execute(query)
        await self.session.commit()
