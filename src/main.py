import uvicorn

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from .schemas import PingResponse
from src.todo.router import router as todo_router

app = FastAPI(
    title="ToDo App",
    debug=True,
    root_path="/api",
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
def index():
    return RedirectResponse("/api/docs")

@app.get("/ping")
def ping() -> PingResponse: 
    return {"result": True}

app.include_router(todo_router, prefix="/v1/todos")

if __name__ == "__main__":
    uvicorn.run(app, reload=True)