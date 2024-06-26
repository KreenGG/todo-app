from datetime import datetime
from pydantic import BaseModel


class TodoAddSchema(BaseModel):
    title: str
    
class TodoDeleteSchema(BaseModel):
    success: bool

class TodoOutSchema(TodoAddSchema):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True