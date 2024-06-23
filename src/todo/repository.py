from abc import ABC, abstractmethod

from fastapi import Depends
from sqlalchemy import select

from src.database import get_session
from .models import Todo
from .schemas import TodoOutResponse

class BaseTodoRepository(ABC):
    @abstractmethod
    async def get_all():
        ...
        

class SQLAlchemyTodoRepository(BaseTodoRepository):
    async def get_all(session=Depends(get_session())):
        async with session:
            query = select(Todo)
            result = await session.execute(query)
            result_orm = result.scalars().all()
            data = [TodoOutResponse.model_validate(row) for row in result_orm]
            return data