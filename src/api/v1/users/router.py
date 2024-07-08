from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from src.api.v1.schemas import ApiResponse
from src.core.users.schemas import (UserLoginSchema, UserOutSchema,
                                    UserRegisterSchema)
from src.core.users.service import BaseUserService, ORMUserService

router = APIRouter()


@router.post(
    "",
    responses={
        status.HTTP_201_CREATED: {"model": ApiResponse[UserOutSchema]},
    },
    status_code=status.HTTP_201_CREATED
)
async def register_user(
    user: UserRegisterSchema,
    service: Annotated[BaseUserService, Depends(ORMUserService)],
) -> ApiResponse[UserOutSchema]:
    created_user = await service.register_user(user)
    return {
        "data": created_user,
        "meta": {}
    }


@router.post("/login")
async def login_user(
    response: Response,
    user: UserLoginSchema,
    service: Annotated[BaseUserService, Depends(ORMUserService)],
):
    token = await service.login_user(user)
    response.set_cookie("access_token", token, httponly=True)
    return {
        "data": {"token": token},
        "meta": {},
    }


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
