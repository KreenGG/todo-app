from datetime import timezone
from sqlalchemy import insert
from src.core.todos.schemas import TodoAddSchema
from src.core.todos.models import TodoModel

from faker import Faker


# ? Пока что фабрика не нужна, но может пригодится
class TodoFactory:
    def __init__(self, session) -> None:
        self.session = session

    async def create_bunch(self, size: int):
        fake = Faker()

        for _ in range(size):
            todo = TodoAddSchema(
                title=fake.first_name(),
                description=fake.text(),
                target_date=fake.date_time_this_month(
                    before_now=False, after_now=True, tzinfo=timezone.utc
                ),
            )

            query = (
                insert(TodoModel)
                .values(**todo.__dict__, user_id=1)
                .returning(TodoModel)
            )
            await self.session.execute(query)
        await self.session.commit()
