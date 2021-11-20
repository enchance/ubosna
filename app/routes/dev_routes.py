from typing import Optional
from fastapi import APIRouter, Response, Query, Path, Depends

from app import settings as s



devroutes = APIRouter()

@devroutes.get('/')
async def index(_: Response):
    return s.TESTDATA


@devroutes.get('/foo/{age}')
async def foo(age: int = Path(..., title='This is Mei-mei', gt=5, example='24')):
    return age





