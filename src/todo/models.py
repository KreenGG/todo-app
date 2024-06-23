from sqlalchemy.orm import Mapped, mapped_column

from src.models import TimedModel

class Todo(TimedModel):
    __tablename__ = "todo"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)