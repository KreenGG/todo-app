from fastapi import APIRouter, Depends, status
from src.schemas import ApiResponse, ErrorApiResponse
from src.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import TodoNotFoundException
from .service import BaseTodoService, ORMTodoService
from .schemas import TodoAddSchema, TodoDeleteSchema, TodoOutSchema

router = APIRouter(tags=["Todo"])

@router.get("")
async def get_todo_list(
    session: AsyncSession = Depends(get_session)
) -> ApiResponse[list[TodoOutSchema]]:
    service: BaseTodoService = ORMTodoService()
    todo_list = await service.get_todo_list(session)
    response = ApiResponse[list[TodoOutSchema]](data=todo_list)
    return response

@router.get(
    "/{id}",
    responses={
        status.HTTP_200_OK: {'model': ApiResponse[TodoOutSchema]},
        status.HTTP_404_NOT_FOUND: {'model': ErrorApiResponse},
    },
)
async def get_single_todo(
    id: int, 
    session: AsyncSession = Depends(get_session)
) -> ApiResponse[TodoOutSchema]:
    service: BaseTodoService = ORMTodoService()
    todo = await service.get_single_todo(session, id)
    if not todo:
        raise TodoNotFoundException
    
    response = ApiResponse[TodoOutSchema](data=todo)
    return response
        
@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
async def create_todo(
    todo: TodoAddSchema, 
    session: AsyncSession = Depends(get_session)
) -> ApiResponse[TodoOutSchema]:
    service: BaseTodoService = ORMTodoService()
    todo = await service.add_todo(session, todo)
    response = ApiResponse[TodoOutSchema](data=todo)
    return response

@router.patch(
    "/{id}",
)
async def update_todo(
    todo: TodoAddSchema, 
    todo_id: int, 
    session: AsyncSession = Depends(get_session)
) :
    service: BaseTodoService = ORMTodoService()
    todo = await service.update_todo(session, todo, todo_id)
    response = ApiResponse[TodoOutSchema](data=todo)
    return response

@router.delete("")
async def delete_todo(
    todo_id: int, 
    session: AsyncSession = Depends(get_session)
) -> ApiResponse[TodoDeleteSchema]:
    service: BaseTodoService = ORMTodoService()
    await service.delete_todo(session, todo_id)
    return ApiResponse[TodoDeleteSchema](data={"success": True})