from typing import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import async_session_maker
from src.core.todos.repository import BaseTodoRepository, SQLAlchemyTodoRepository
from src.core.todos.service import BaseTodoService, ORMTodoService
from src.core.users.repository import BaseUserRepository, SQLAlchemyUserRepository
from src.core.users.service import BaseUserService, ORMUserService


class MainProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def session(self) -> AsyncIterable[AsyncSession]:
        async with async_session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    async def get_todo_repository(self, session: AsyncSession) -> BaseTodoRepository:
        return SQLAlchemyTodoRepository(session)

    @provide(scope=Scope.REQUEST)
    async def get_todo_service(self, repo: BaseTodoRepository) -> BaseTodoService:
        return ORMTodoService(repo)

    @provide(scope=Scope.REQUEST)
    async def get_user_repository(self, session: AsyncSession) -> BaseUserRepository:
        return SQLAlchemyUserRepository(session)

    @provide(scope=Scope.REQUEST)
    async def get_user_service(self, repo: BaseUserRepository) -> BaseUserService:
        return ORMUserService(repo)
