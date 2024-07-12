from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Todo:
    id: int
    title: str
    description: Optional[str]
    target_date: Optional[datetime]
    user_id: int
    created_at: datetime
    updated_at: datetime
