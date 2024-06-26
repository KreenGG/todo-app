from abc import ABC, abstractmethod
from typing import Iterable
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import TodoAddSchema

from .repository import BaseTodoRepository, SQLAlchemyTodoRepository

from .entities import Todo


class BaseTodoService(ABC):
    @abstractmethod
    async def get_todo_list(self, session) -> Iterable[Todo]:
        raise NotImplementedError
    
    @abstractmethod
    async def get_single_todo(self, session, todo_id: int) -> Todo:
        raise NotImplementedError
    
    @abstractmethod
    async def add_todo(self, session, todo: TodoAddSchema) -> Todo:
        raise NotImplementedError
    
    @abstractmethod
    async def update_todo(self, session, todo: TodoAddSchema, todo_id: int) -> Todo:
        raise NotImplementedError
    
    @abstractmethod
    async def delete_todo(self, session, todo_id: int) -> None:
        raise NotImplementedError


class ORMTodoService(BaseTodoService):
    async def get_todo_list(self, session: AsyncSession) -> Iterable[Todo]:
        repo: BaseTodoRepository = SQLAlchemyTodoRepository()
        todo_list = await repo.get_all(session)
        return todo_list
    
    async def get_single_todo(self, session, todo_id: int) -> Todo:
        repo: BaseTodoRepository = SQLAlchemyTodoRepository()
        todo = await repo.get_single(session, todo_id)
        return todo
    
    async def add_todo(self, session: AsyncSession, todo: TodoAddSchema) -> Todo:
        repo: BaseTodoRepository = SQLAlchemyTodoRepository()
        todo = await repo.add(session, todo)
        return todo
    
    async def update_todo(self, session, todo: TodoAddSchema, todo_id: int) -> Todo:
        repo: BaseTodoRepository = SQLAlchemyTodoRepository()
        todo = await repo.update(session, todo, todo_id)
        return todo
    
    async def delete_todo(self, session: AsyncSession, todo_id: int) -> None:
        repo: BaseTodoRepository = SQLAlchemyTodoRepository()
        await repo.delete(session, todo_id)