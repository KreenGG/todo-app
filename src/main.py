from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1 import router as v1_router
from .api.v1.schemas import PingResponse
from .dependencies import MainProvider


def create_app() -> FastAPI:
    app = FastAPI(
        title="ToDo App",
        debug=True,
        root_path="/api",
    )

    app.include_router(v1_router)

    @app.get("/ping")
    def ping() -> PingResponse:
        return {"result": True}

    return app


def create_production_app() -> FastAPI:
    app = create_app()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    container = make_async_container(MainProvider())
    setup_dishka(container, app)

    return app


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(factory=create_production_app, reload=True, app_dir="..")
