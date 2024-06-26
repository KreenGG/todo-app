from dataclasses import dataclass
from datetime import datetime


@dataclass
class Todo():
    id: int
    title: str
    created_at: datetime
    updated_at: datetime