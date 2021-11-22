from typing import Optional
from fastapi import Request, Depends
from fastapi_users import FastAPIUsers, BaseUserManager
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import TortoiseUserDatabase

from app import settings as s, ic
from .authentication.models.account import Account
from .authentication.models.pydantic import User, UserCreate, UserUpdate, UserDB




class UserManager(BaseUserManager[UserCreate, UserDB]):
    user_db_model = UserDB
    reset_password_token_secret = s.SECRET_KEY
    verification_token_secret = s.SECRET_KEY

    # async def on_after_register(self, user: UserDB, request: Optional[Request] = None):
    #     ic(f"User {user.id} has registered.")
    #
    # async def on_after_forgot_password(
    #         self, user: UserDB, token: str, request: Optional[Request] = None
    # ):
    #     ic(f"User {user.id} has forgot their password. Reset token: {token}")
    #
    # async def on_after_request_verify(
    #         self, user: UserDB, token: str, request: Optional[Request] = None
    # ):
    #     ic(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_db():
    yield TortoiseUserDatabase(UserDB, Account)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


jwtauth = JWTAuthentication(secret=s.SECRET_KEY, lifetime_seconds=s.ACCESS_TOKEN_EXPIRE)
fusers = FastAPIUsers(get_user_manager, [jwtauth], User, UserCreate, UserUpdate, UserDB)
current_user = fusers.current_user()

