from datetime import date
from typing import Optional
from fastapi_users import models
from tortoise.contrib.pydantic import PydanticModel
from pydantic import BaseModel, Field, validator

from app import settings as s
from .account import Account


class User(models.BaseUser):
    username: Optional[str] = Field('', le=50)
    display: Optional[str] = Field('', le=50)
    timezone: Optional[str] = Field('', le=10)
    currency: Optional[str] = Field('', le=5)


class UserCreate(models.BaseUserCreate):
    @validator('password')
    def valid_password(cls, v: str):
        if len(v) < s.PASSWORD_MIN:
            raise ValueError(f'Password should be at least {s.PASSWORD_MIN} characters')
        return v


class UserUpdate(models.BaseUserUpdate):
    pass


class AccountDB(User, models.BaseUserDB):
    """
    Represents the actual Account table. Use this to parse Account.
    """
    firstname: Optional[str] = Field('', le=191)
    midname: Optional[str] = Field('', le=191)
    lastname: Optional[str] = Field('', le=191)
    civil: Optional[str] = Field('', le=20)
    bday: Optional[date] = None
    status: Optional[str] = Field('', le=20)
    country: Optional[str] = Field('', le=2)
    bio: Optional[str] = Field('', le=191)
    zipcode: Optional[str] = Field('', le=20)
    metadata: Optional[dict] = None
    
    # class Config:
    #     orm_mode = True
    #     orig_model = Account