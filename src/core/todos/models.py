from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.models import TimedModel

from .entities import Todo


class TodoModel(TimedModel):
    __tablename__ = "todo"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    target_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    def to_entity(self) -> Todo:
        return Todo(
            id=self.id,
            title=self.title,
            description=self.description,
            target_date=self.target_date,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    # @staticmethod
    # def from_entity(todo: Todo) -> "TodoModel":
    #     return TodoModel(
    #         id=todo.id,
    #         title=todo.title,
    #         description=todo.description,
    #         target_date=todo.target_date,
    #         created_at=todo.created_at,
    #         updated_at=todo.updated_at,
    #     ) # noqa
