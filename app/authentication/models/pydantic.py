from datetime import date
from typing import Optional
from fastapi_users import models
from tortoise.contrib.pydantic import PydanticModel
from pydantic import BaseModel, Field, validator

from app import settings as s
from .account import Account


class User(models.BaseUser):
    """
    Data you want visible in the current_user dependency. Each must have a default value or
    the sky will fall on your head, you'll go blind, and you'll get a girlfriend.
    """
    username: str = ''
    timezone: str = s.USER_TIMEZONE
    lang: str = 'en'
    display: str = ''
    currency: str = s.CURRENCY_ACCOUNT
    

class UserCreate(models.BaseUserCreate):
    """
    Data pydantic will take from the form.
    """
    username: Optional[str]
    @validator('password')
    def valid_password(cls, v: str):
        if len(v) < s.PASSWORD_MIN:
            raise ValueError(f'Password should be at least {s.PASSWORD_MIN} characters')
        return v


class UserUpdate(models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB, PydanticModel):
    # display: str
    # username: Optional[str] = ''
    # firstname: Optional[str] = ''
    # midname: Optional[str] = ''
    # lastname: Optional[str] = ''
    # civil: Optional[str] = ''
    # bday: Optional[date] = None
    # status: Optional[str] = ''
    # country: Optional[str] = ''
    # bio: Optional[str] = ''
    # zipcode: Optional[str] = ''
    # metadata: Optional[dict] = None

    class Config:
        orm_mode = True
        orig_model = Account
