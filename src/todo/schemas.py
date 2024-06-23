from datetime import datetime
from pydantic import BaseModel


class TodoOutResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True