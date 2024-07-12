from datetime import datetime
from typing import Optional

from pydantic import BaseModel, FutureDatetime


class TodoAddSchema(BaseModel):
    title: str
    description: Optional[str]
    target_date: FutureDatetime


class TodoUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    target_date: Optional[FutureDatetime] = None


class TodoOutSchema(TodoAddSchema):
    model_config = {"from_attributes": True}

    id: int
    created_at: datetime
    updated_at: datetime
