from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserOutSchema(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserRegisterSchema(UserLoginSchema):
    pass
