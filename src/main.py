from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .schemas import PingResponse
from src.todo.router import router as todo_router

app = FastAPI(
    title="ToDo App",
    debug=True,
    root_path="/api"
    )

@app.get("/", include_in_schema=False)
def index():
    return RedirectResponse("/api/docs")

@app.get("/ping")
def ping() -> PingResponse: 
    return {"result": True}

app.include_router(todo_router, prefix="/todo")