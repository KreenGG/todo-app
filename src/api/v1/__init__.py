from fastapi import APIRouter

from .todos.router import router as todo_router

router = APIRouter(
    prefix="/v1",
)

router.include_router(
    todo_router,
    prefix="/todos",
    tags=["Todo"],
)
