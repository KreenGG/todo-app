from fastapi import APIRouter, Depends, status

from src.api.v1.schemas import ApiResponse, ErrorApiResponse
from src.core.todos.schemas import (TodoAddSchema, TodoDeleteSchema,
                                    TodoOutSchema, TodoUpdateSchema)
from src.core.todos.service import BaseTodoService, ORMTodoService

from .exceptions import TodoNotFoundException

router = APIRouter()


@router.get("")
async def get_todo_list(
    service: BaseTodoService = Depends(ORMTodoService),
) -> ApiResponse[list[TodoOutSchema]]:
    todo_list = await service.get_todo_list()
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
    service: BaseTodoService = Depends(ORMTodoService),
) -> ApiResponse[TodoOutSchema]:
    todo = await service.get_single_todo(id)
    if not todo:
        raise TodoNotFoundException

    response = ApiResponse[TodoOutSchema](data=todo)
    return response


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def create_todo(
    todo: TodoAddSchema,
    service: BaseTodoService = Depends(ORMTodoService),
) -> ApiResponse[TodoOutSchema]:
    todo = await service.add_todo(todo)
    response = ApiResponse[TodoOutSchema](data=todo)
    return response


@router.patch(
    "/{id}",
    responses={
        status.HTTP_200_OK: {'model': ApiResponse[TodoOutSchema]},
        status.HTTP_404_NOT_FOUND: {'model': ErrorApiResponse},
    },
)
async def update_todo(
    todo: TodoUpdateSchema,
    id: int,
    service: BaseTodoService = Depends(ORMTodoService),
):
    todo = await service.update_todo(todo, id)
    if not todo:
        raise TodoNotFoundException
    response = ApiResponse[TodoOutSchema](data=todo)
    return response


@router.delete("/{id}")
async def delete_todo(
    id: int,
    service: BaseTodoService = Depends(ORMTodoService),
) -> ApiResponse[TodoDeleteSchema]:
    await service.delete_todo(id)
    return ApiResponse[TodoDeleteSchema](data={"success": True})
