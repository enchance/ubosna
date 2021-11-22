from typing import Optional, Union
from fastapi import APIRouter, Response, Query, Path, Depends

from app import settings as s



devrouter = APIRouter()

@devrouter.get('/')
async def index(_: Response):
    return s.TESTDATA

@devrouter.get('/foo/{age}')
async def foo(age: int = Path(..., ge=5, title='This is Mei-mei')) -> int:
    return age

@devrouter.post("/cookie/")
def create_cookie(res: Response):
    res.set_cookie(key="fakesession", value="fake-cookie-session-value")
    res.set_cookie(key="fruit", value="apple")
    res.headers["X-Cat-Dog"] = "alone in the world"
    return {"message": "Come to the dark side, we have cookies"}

