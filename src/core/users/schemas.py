from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserOutSchema(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class UserRegisterSchema(UserLoginSchema):
    pass
