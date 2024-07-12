from abc import ABC, abstractmethod
from typing import Iterable

from dishka.integrations.fastapi import FromDishka

from src.core.users.entities import User

from .entities import Todo
from .repository import BaseTodoRepository
from .schemas import TodoAddSchema, TodoUpdateSchema


class BaseTodoService(ABC):
    @abstractmethod
    async def get_todo_list(self, user: User) -> Iterable[Todo]:
        raise NotImplementedError

    @abstractmethod
    async def get_single_todo(self, user: User, todo_id: int) -> Todo:
        raise NotImplementedError

    @abstractmethod
    async def add_todo(self, user: User, todo: TodoAddSchema) -> Todo:
        raise NotImplementedError

    @abstractmethod
    async def update_todo(self, user: User, todo: TodoAddSchema, todo_id: int) -> Todo:
        raise NotImplementedError

    @abstractmethod
    async def delete_todo(self, user: User, todo_id: int) -> None:
        raise NotImplementedError


class ORMTodoService(BaseTodoService):
    def __init__(self, repo: FromDishka[BaseTodoRepository]) -> None:
        self.repo = repo

    async def get_todo_list(
        self,
        user: User,
    ) -> Iterable[Todo]:
        todo_list = await self.repo.find_all(user)
        return todo_list

    async def get_single_todo(self, user: User, todo_id: int) -> Todo:
        todo = await self.repo.find_by_id(user, todo_id)
        return todo

    async def add_todo(self, user: User, todo: TodoAddSchema) -> Todo:
        todo = await self.repo.add(user, todo)
        return todo

    async def update_todo(
        self, user: User, todo: TodoUpdateSchema, todo_id: int
    ) -> Todo:
        todo_obj = await self.repo.find_by_id(user, todo_id)
        if not todo_obj:
            return None

        updated_data = todo.model_dump(exclude_unset=True)
        updated_todo = await self.repo.update(user, updated_data, todo_id)
        return updated_todo

    async def delete_todo(self, user: User, todo_id: int) -> None:
        await self.repo.delete(user, todo_id)
