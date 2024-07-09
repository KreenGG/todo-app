from abc import ABC, abstractmethod
from typing import Iterable

from fastapi import Depends

from .entities import Todo
from .repository import BaseTodoRepository
from .schemas import TodoAddSchema, TodoUpdateSchema


class BaseTodoService(ABC):
    @abstractmethod
    async def get_todo_list(self) -> Iterable[Todo]:
        raise NotImplementedError

    @abstractmethod
    async def get_single_todo(self, todo_id: int) -> Todo:
        raise NotImplementedError

    @abstractmethod
    async def add_todo(self, todo: TodoAddSchema) -> Todo:
        raise NotImplementedError

    @abstractmethod
    async def update_todo(self, todo: TodoAddSchema, todo_id: int) -> Todo:
        raise NotImplementedError

    @abstractmethod
    async def delete_todo(self, todo_id: int) -> None:
        raise NotImplementedError


class ORMTodoService(BaseTodoService):
    def __init__(
        self,
        repo: BaseTodoRepository = Depends(),
    ) -> None:
        self.repo = repo

    async def get_todo_list(
        self,
    ) -> Iterable[Todo]:
        todo_list = await self.repo.find_all()
        return todo_list

    async def get_single_todo(self, todo_id: int) -> Todo:
        todo = await self.repo.find_by_id(todo_id)
        return todo

    async def add_todo(self, todo: TodoAddSchema) -> Todo:
        todo = await self.repo.add(todo)
        return todo

    async def update_todo(self, todo: TodoUpdateSchema, todo_id: int) -> Todo:
        todo_obj = await self.repo.find_by_id(todo_id)
        if not todo_obj:
            return None

        updated_data = todo.model_dump(exclude_unset=True)
        updated_todo = await self.repo.update(updated_data, todo_id)
        return updated_todo

    async def delete_todo(self, todo_id: int) -> None:
        await self.repo.delete(todo_id)
