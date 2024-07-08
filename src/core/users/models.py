from datetime import datetime, timezone

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models import Base
from src.core.users.entities import User


class UserModel(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        nullable=False,
    )

    def to_entity(self) -> User:
        return User(
            id=self.id,
            email=self.email,
            hashed_password=self.hashed_password,
            created_at=self.created_at,
        )
