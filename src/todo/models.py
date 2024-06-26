from sqlalchemy.orm import Mapped, mapped_column

from src.models import TimedModel
from .entities import Todo

class TodoModel(TimedModel):
    __tablename__ = "todo"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)

    def to_entity(self) -> Todo:
        return Todo(
            id=self.id,
            title=self.title,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )