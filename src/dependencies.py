from fastapi import FastAPI

from src.core.database import get_session, get_session_stub
from src.core.todos.repository import (BaseTodoRepository,
                                       SQLAlchemyTodoRepository)
from src.core.todos.service import BaseTodoService, ORMTodoService
from src.core.users.repository import (BaseUserRepository,
                                       SQLAlchemyUserRepository)
from src.core.users.service import BaseUserService, ORMUserService


def init_dependencies(app: FastAPI) -> None:
    app.dependency_overrides[get_session_stub] = get_session

    app.dependency_overrides[BaseTodoService] = ORMTodoService
    app.dependency_overrides[BaseTodoRepository] = SQLAlchemyTodoRepository

    app.dependency_overrides[BaseUserService] = ORMUserService
    app.dependency_overrides[BaseUserRepository] = SQLAlchemyUserRepository
