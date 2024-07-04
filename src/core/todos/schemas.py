from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TodoAddSchema(BaseModel):
    title: str
    description: Optional[str]
    target_date: datetime


class TodoUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    target_date: Optional[datetime] = None


class TodoDeleteSchema(BaseModel):
    success: bool


class TodoOutSchema(TodoAddSchema):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
