from fastapi import APIRouter, Response, Request, HTTPException, status, Depends
from fastapi_users import models
from fastapi_users.router.common import ErrorCode
from fastapi_users.manager import BaseUserManager, InvalidPasswordException, UserAlreadyExists

from app import ic
from app.auth import fusers, User, UserCreate, get_user_manager



authrouter = APIRouter()


@authrouter.post("/register", response_model=User, status_code=201, name="register:register")
async def register(request: Request, user: UserCreate, user_manager=Depends(get_user_manager)):
    ic(user)
    try:
        created_user = await user_manager.create(user, safe=True, request=request)
    except UserAlreadyExists:
        raise HTTPException(status_code=400, detail=ErrorCode.REGISTER_USER_ALREADY_EXISTS)
    except InvalidPasswordException as e:
        raise HTTPException(
            status_code=400,
            detail={
                "code": ErrorCode.REGISTER_INVALID_PASSWORD,
                "reason": e.reason,
            },
        )
    ic(created_user)
    return created_user


@authrouter.get("/logout")
async def logout(response: Response):
    """
    Logout the user by deleting all tokens.
    """
    del response.headers['authorization']
    response.delete_cookie('refresh_token')
    return