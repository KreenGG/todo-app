from collections.abc import AsyncGenerator
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
import pytest
from httpx import ASGITransport, AsyncClient, Response
from faker import Faker

from src.dependencies import MainProvider
from src.core.models import Base
from src.main import create_app


from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine
from src.config import settings
from tests.dependencies import TestProvider

engine_test = create_async_engine(
    url=str(settings.test_db.url),
    echo=True,
    poolclass=NullPool,  # Нужен чтобы избежать RuntimeError Task attached to a different loop
)


@pytest.fixture(scope="session")
async def container():
    container = make_async_container(MainProvider(), TestProvider(engine_test))
    yield container
    await container.close()


@pytest.fixture(scope="session")
def app(container) -> FastAPI:
    app = create_app()
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


@pytest.fixture(scope="function")
async def authenticated_ac(app):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        faker = Faker()
        body = {
            "email": faker.email(),
            "password": faker.password(length=10),
        }
        await ac.post("/api/v1/auth/register", json=body)
        response: Response = await ac.post("/api/v1/auth/login", json=body)

        assert response.cookies.get("access_token")
        yield ac
