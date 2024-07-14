from collections.abc import AsyncGenerator
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
import pytest
from httpx import ASGITransport, AsyncClient

from src.dependencies import MainProvider
from src.core.models import Base
from src.main import create_app


from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine
from src.config import settings
from tests.dependencies import TestProvider

engine_test = create_async_engine(
    url=str(settings.test_db.url),
    echo=False,
    poolclass=NullPool,  # Нужен чтобы избежать RuntimeError Task attached to a different loop
)


@pytest.fixture
def app() -> FastAPI:
    app = create_app()
    container = make_async_container(MainProvider(), TestProvider(engine_test))
    setup_dishka(container, app)
    return app


@pytest.fixture(scope="session", autouse=True)
async def create_tables():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


@pytest.fixture(scope="function")
async def ac(app) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
