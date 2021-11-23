import contextlib
from typing import Optional
from operator import itemgetter
from fastapi import Request, Depends
from fastapi_users import FastAPIUsers, BaseUserManager
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import TortoiseUserDatabase
from fastapi_users.manager import UserAlreadyExists
from pydantic import EmailStr

from app import settings as s, ic
from .authentication.models.account import Account
from .authentication.models.pydantic import User, UserCreate, UserUpdate, UserDB


# INCOMPLETE: Work in progress...
def setup_account(account: Account, user: UserDB):
    email, username = itemgetter('email', 'username')(user.dict())
    account.display = username and username or user.email.split('@')[0]
    return account


# INCOMPLETE: Work in progress...
async def setup_groups(account: Account):
    # Get the ids of the default groups
    # Add groups to the user
    pass


# INCOMPLETE: Work in progress...
async def setup_options(account: Account):
    # ll = []
    # for name, val in options_dict['user'].items():
    #     ll.append(Option(name=name, value=val, user=usermod))
    # await Option.bulk_create(ll)
    pass


class UserManager(BaseUserManager[UserCreate, UserDB]):
    user_db_model = UserDB
    reset_password_token_secret = s.SECRET_KEY
    verification_token_secret = s.SECRET_KEY

    async def on_after_register(self, user: UserDB, request: Optional[Request] = None):
        # ic(f"User {user.id} has registered.")
        account = await Account.get(id=user.id).only('id', 'display')
        
        account = setup_account(account, user)
        await account.save(update_fields=['display'])
        
        await setup_groups(account)
        await setup_options(account)
        
        # Generate verification token which triggers on_after_request_verify()
        await self.request_verify(user, request)

    # async def on_after_forgot_password(
    #         self, user: UserDB, token: str, request: Optional[Request] = None
    # ):
    #     ic(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(self, user: UserDB, token: str, request: Optional[Request] = None):
        # ic(f"Verification requested for user {user.id}. Verification token: {token}")
        ic('Send the email to verify.')


async def get_user_db():
    yield TortoiseUserDatabase(UserDB, Account)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)

async def create_user(email: str, password: str, *, username: str = '', is_superuser: bool = False):
    """Programmatically create a user"""
    try:
        async with get_user_db_context() as user_db:
            async with get_user_manager_context(user_db) as user_manager:
                created_user = await user_manager.create(
                    UserCreate(email=EmailStr(email), password=password, username=username,
                               is_superuser=is_superuser)
                )
                return created_user.email
    except UserAlreadyExists:
        pass

jwtauth = JWTAuthentication(secret=s.SECRET_KEY, lifetime_seconds=s.ACCESS_TOKEN_EXPIRE)
fusers = FastAPIUsers(get_user_manager, [jwtauth], User, UserCreate, UserUpdate, UserDB)
current_user = fusers.current_user()