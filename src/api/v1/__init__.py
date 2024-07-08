from fastapi import APIRouter

from .todos.router import router as todos_router
from .users.router import router as users_router

router = APIRouter(
    prefix="/v1",
)

router.include_router(
    todos_router,
    prefix="/todos",
    tags=["Todos"],
)

router.include_router(
    users_router,
    prefix="/users",
    tags=["Users"],
)
