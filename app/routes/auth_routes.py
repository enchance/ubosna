from fastapi import APIRouter, Response, Request, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import models
from fastapi_users.router.common import ErrorCode
from fastapi_users.manager import BaseUserManager, InvalidPasswordException, UserAlreadyExists

from app import ic
from app import settings as s
from app.auth import jwtauth, User, UserCreate, UserDB, get_user_manager, fusers, Account



authrouter = APIRouter()
authrouter.include_router(fusers.get_register_router())


@authrouter.post("/login", name="auth:login")
async def login(
        response: Response, credentials: OAuth2PasswordRequestForm = Depends(),
        user_manager: BaseUserManager[models.UC, models.UD] = Depends(get_user_manager),
):
    # TODO: Check if active user
    # TODO: Check if verified user
    user = await user_manager.authenticate(credentials)
    if user is None or not user.is_active:
        raise HTTPException(status_code=400, detail=ErrorCode.LOGIN_BAD_CREDENTIALS)
    if s.REQUIRES_VERIFICATION and not user.is_verified:
        raise HTTPException(status_code=400, detail=ErrorCode.LOGIN_USER_NOT_VERIFIED)
    
    # Cache
    # Account.get_and_cache(user.id)
    
    return await jwtauth.get_login_response(user, response, user_manager)


@authrouter.get('/logout')
async def logout(res: Response):
    """
    Logout the user by deleting all tokens.
    """
    del res.headers['authorization']
    res.delete_cookie('refresh_token')
    return