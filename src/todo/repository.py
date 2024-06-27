from abc import ABC, abstractmethod
from typing import Iterable
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import TodoAddSchema

from .entities import Todo

from .models import TodoModel


class BaseTodoRepository(ABC):
    @abstractmethod
    async def find_all(self, session) -> Iterable[Todo]:
        raise NotImplementedError
    
    @abstractmethod
    async def find_by_id(self, session, todo_id: int) -> Todo:
        raise NotImplementedError
    
    @abstractmethod
    async def add(self, session, todo: TodoAddSchema) -> Todo:
        raise NotImplementedError
    
    @abstractmethod
    async def update(self, session, todo: TodoAddSchema, todo_id: int) -> Todo:
        raise NotImplementedError
    
    @abstractmethod
    async def delete(self, session, todo_id: int) -> None:
        raise NotImplementedError
        

class SQLAlchemyTodoRepository(BaseTodoRepository):
    async def find_all(self, session: AsyncSession) -> Iterable[Todo]:
        query = select(TodoModel).order_by(TodoModel.created_at)
        result = await session.execute(query)
        result_orm = result.scalars().all()

        todo_list = [row.to_entity() for row in result_orm]
        return todo_list
    
    async def find_by_id(self, session: AsyncSession, todo_id: int) -> Todo:
        query = select(TodoModel).where(TodoModel.id == todo_id)
        result = await session.execute(query)
        result_orm = result.scalars().first()

        if not result_orm:
            return None
        todo = result_orm.to_entity()
        return todo

    async def add(self, session: AsyncSession, todo: TodoAddSchema) -> Todo:
        query = insert(TodoModel).values(**todo.__dict__).returning(TodoModel)
        result = await session.execute(query)
        await session.commit()
        return result.scalar_one().to_entity()
    
    async def update(self, session: AsyncSession, todo: dict, todo_id: int) -> Todo:
        query = update(TodoModel).where(TodoModel.id == todo_id).values(**todo).returning(TodoModel)
        result = await session.execute(query)
        await session.commit()
        return result.scalar_one().to_entity()
    
    async def delete(self, session: AsyncSession, todo_id: int) -> None:
        query = delete(TodoModel).where(TodoModel.id == todo_id)
        await session.execute(query)
        await session.commit()