from fastapi_users import models
from tortoise.contrib.pydantic import PydanticModel

from .account import Account


class User(models.BaseUser):
    pass


class UserCreate(models.BaseUserCreate):
    pass


class UserUpdate(models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    # class Config:
    #     orm_mode = True
    #     orig_model = Account
    pass