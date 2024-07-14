from typing import AsyncIterable

from dishka import BaseScope, Provider, Scope, provide


from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, AsyncEngine


class TestProvider(Provider):
    def __init__(
        self,
        engine: AsyncEngine,
        scope: BaseScope | None = None,
        component: str | None = None,
    ):
        super().__init__(scope, component)
        self.engine = engine

    @provide(scope=Scope.REQUEST)
    async def session(self) -> AsyncIterable[AsyncSession]:
        async_session_maker = async_sessionmaker(self.engine, expire_on_commit=False)
        async with async_session_maker() as session:
            yield session
