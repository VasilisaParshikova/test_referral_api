from datetime import datetime

from pydantic import BaseModel, EmailStr
from typing import Union


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserAnswer(UserBase):
    id: int
    referr_id: Union[int, None] = None


class UserList(BaseModel):
    users: list[UserAnswer]


class ReferralCode(BaseModel):
    id: int
    code: str
    expired_date: datetime
    user_id: int


class BoolResponse(BaseModel):
    result: bool


class Token(BaseModel):
    access_token: str
    token_type: str
