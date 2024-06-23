from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base

class TimedModel(Base):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(default=datetime.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(), nullable=False, onupdate=datetime.now())