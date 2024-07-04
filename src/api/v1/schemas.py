from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T", bound=BaseModel)


class PingResponse(BaseModel):
    result: bool


class ApiResponse(BaseModel, Generic[T]):
    data: Optional[T] = Field(default_factory=dict)
    meta: Optional[dict] = Field(default_factory=dict)


class ErrorApiResponse(BaseModel):
    detail: str
