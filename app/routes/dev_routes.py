from typing import Optional
from fastapi import APIRouter, Response, Query

from app import settings as s



devroutes = APIRouter()


@devroutes.get('/')
async def index(_: Response):
    return s.TESTDATA


@devroutes.get('/foo')
async def foo(q: Optional[list] = Query(['foo', 'bar'], deprecated=True)):
    return q