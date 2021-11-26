from fastapi import Depends, Request, Body, Header
from tortoise.query_utils import Q
from fastapi_users.manager import UserAlreadyExists
from pydantic import EmailStr

from app import settings as s, exceptions as x
from app.auth import Account, get_user_manager




async def is_unique_username(_: Request, username: str = Body(...)):
    if await Account.exists(username=username):
        raise UserAlreadyExists
        

async def is_unique_email(_: Request, email: EmailStr = Body(...)):
    if await Account.exists(email=email):
        raise UserAlreadyExists


# async def verify_key(x_key: str = Header(...)):
#     if x_key != 'xxx':
#         raise x.GenericError()