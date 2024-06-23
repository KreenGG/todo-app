
from pydantic import BaseModel, Field
from typing import Generic, Optional, TypeVar


T = TypeVar("T", bound=BaseModel)

class PingResponse(BaseModel):
    result: bool
    
    
class ApiResponse(BaseModel, Generic[T]):
    data: Optional[T] = Field(default_factory=dict)
    meta: Optional[dict] = Field(default_factory=dict)
