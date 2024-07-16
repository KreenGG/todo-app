from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Request, status

from src.core.users.service import BaseUserService
from src.api.v1.schemas import ApiResponse, ErrorApiResponse
from src.core.todos.schemas import TodoAddSchema, TodoOutSchema, TodoUpdateSchema
from src.core.todos.service import BaseTodoService

from .exceptions import TodoNotFoundException

router = APIRouter(route_class=DishkaRoute)


@router.get(
    "",
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[list[TodoOutSchema]]},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorApiResponse},
    },
)
async def get_todo_list(
    todo_service: FromDishka[BaseTodoService],
    user_service: FromDishka[BaseUserService],
    request: Request,
) -> ApiResponse[list[TodoOutSchema]]:
    user = await user_service.get_current_user(request)
    todo_list = await todo_service.get_todo_list(user)
    response = ApiResponse[list[TodoOutSchema]](data=todo_list)
    return response


@router.get(
    "/{id}",
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[TodoOutSchema]},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorApiResponse},
        status.HTTP_404_NOT_FOUND: {"model": ErrorApiResponse},
    },
)
async def get_single_todo(
    id: int,
    todo_service: FromDishka[BaseTodoService],
    user_service: FromDishka[BaseUserService],
    request: Request,
) -> ApiResponse[TodoOutSchema]:
    user = await user_service.get_current_user(request)
    todo = await todo_service.get_single_todo(user, id)
    if not todo:
        raise TodoNotFoundException

    response = ApiResponse[TodoOutSchema](data=todo)
    return response


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": ApiResponse[TodoOutSchema]},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorApiResponse},
    },
)
async def create_todo(
    todo: TodoAddSchema,
    todo_service: FromDishka[BaseTodoService],
    user_service: FromDishka[BaseUserService],
    request: Request,
) -> ApiResponse[TodoOutSchema]:
    user = await user_service.get_current_user(request)

    todo = await todo_service.add_todo(user, todo)

    response = ApiResponse[TodoOutSchema](data=todo)
    return response


# TODO: Поменять на PUT, ибо так будет более интуитивно
@router.patch(
    "/{id}",
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[TodoOutSchema]},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorApiResponse},
        status.HTTP_404_NOT_FOUND: {"model": ErrorApiResponse},
    },
)
async def update_todo(
    todo: TodoUpdateSchema,
    id: int,
    todo_service: FromDishka[BaseTodoService],
    user_service: FromDishka[BaseUserService],
    request: Request,
):
    user = await user_service.get_current_user(request)

    todo = await todo_service.update_todo(user, todo, id)
    if not todo:
        raise TodoNotFoundException
    response = ApiResponse[TodoOutSchema](data=todo)
    return response


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorApiResponse},
    },
)
async def delete_todo(
    id: int,
    todo_service: FromDishka[BaseTodoService],
    user_service: FromDishka[BaseUserService],
    request: Request,
) -> None:
    user = await user_service.get_current_user(request)
    await todo_service.delete_todo(user, id)
    return None
