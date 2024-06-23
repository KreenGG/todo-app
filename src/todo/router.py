from fastapi import APIRouter
from sqlalchemy import insert, select, update
from src.schemas import ApiResponse
from src.database import async_session
from .schemas import TodoOutResponse

from .models import Todo

router = APIRouter(tags=["Todo"])

@router.get("", response_model=ApiResponse[list[TodoOutResponse]])
async def get_all_todos():
    async with async_session() as session:
        query = select(Todo)
        result = await session.execute(query)
        result_orm = result.scalars().all()
        data = [TodoOutResponse.model_validate(row) for row in result_orm]
        
        response = ApiResponse[list[TodoOutResponse]](data=data)
        return response

        
@router.post("")
async def create_todo(title: str):
    async with async_session() as session:
        query = insert(Todo).values({"title": title})
        await session.execute(query)
        await session.commit()
        return "success"

@router.put("/{id}")
async def update_todo(id: int, title: str):
    async with async_session() as session:
        query = update(Todo).where(Todo.id == id).values({"title": title})
        await session.execute(query)
        await session.commit()
        return "success"