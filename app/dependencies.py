from fastapi import Depends, Request, Body, Header
from pydantic import EmailStr

from app import settings as s, exceptions as x


# INCOMPLETE: Work in progress...
async def is_unique_account(_: Request, email: EmailStr = Body(...), username: str = Body(...)):
    # if await UserMod.exists(Q(username=username) | Q(email=email)):
    #     raise x.UnusableDataError('ACCOUNT ALREADY EXISTS')
    return True


# INCOMPLETE: Work in progress...
async def verify_key(x_key: str = Header(...)):
    if x_key != 'xxx':
        raise x.GenericError()