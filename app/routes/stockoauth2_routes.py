from typing import Optional
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from app import ic


authroutes = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_users_db = {
    "enchance": {
        "username": "enchance",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "pass1",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "pass2",
        "disabled": True,
    },
}

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    ic(user)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@authroutes.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """This just returns a token. Nothing more."""
    user_dict = fake_users_db.get(form_data.username)
    # ic(user_dict)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = form_data.password
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    return {"access_token": user.username, "token_type": "bearer"}


@authroutes.get("/private")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Use the token taken from /token"""
    return current_user
