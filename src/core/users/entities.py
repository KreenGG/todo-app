from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: int
    email: str
    hashed_password: str
    created_at: datetime
