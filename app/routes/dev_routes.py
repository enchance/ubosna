from typing import Optional, Union, List
from fastapi import APIRouter, Response, Query, Path, Depends
from tortoise.query_utils import Prefetch, Q
from pydantic import validate_arguments

from app import settings as s, ic
from app.auth import current_user
from app.authentication.models.account import Group, Perm, Account
from app.authentication.models.common import Option


devrouter = APIRouter()

@validate_arguments
def foobar(*args: str):
    return args

@devrouter.get('/')
async def index(_: Response):
    return foobar('a', 'b')
    
    # id = '684f0bf2-bb11-4405-a7ca-a217c39b6771'
    # account = await Account.get(id=id)
    
    # return await Account.get_and_cache(account.id)
    
    # perms1 = await Perm.get_perms('AccountGroup')
    # perms2 = await Perm.get_perms('TradeGroup')
    # perms3 = await Perm.get_perms('ModGroupSet')
    # return [(perms1 + perms2), perms3]
    
    # # return await account.has_perm('trade.make')
    # # return await account.has_perm('account.ban')
    
    # data1 = await account.get_groups()
    # data1 = await Perm.get_perms(*data1)
    # await account.add_group('ModGroupSet')
    # data2 = await account.get_groups()
    # data2 = await Perm.get_perms(*data2)
    # return [data1, data2]
    
    # return await account.get
    # dbperms = await Perm.filter(permgroups__name__in=['AccountGroup'])\
    #     .values_list('code', flat=True)
    # return dbperms
    # perms = await Perm.get_perms('AccountGroup', 'ModGroupSet')
    # return perms

    # return await Group.filter(name__in={'AccountGroup', 'TradeGroup'}).only('id', 'name')
    
    # if y := []:
    #     ic('foo')
    # else:
    #     y = 'x'
    #     ic(y)
    # ic(y)
    
    # x = await Account.all().values_list('id', flat=True)
    # x = await Account.filter(Q(accountoptions=None)).distinct().values_list('id', flat=True)
    # return x
    
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

@devrouter.get('/private')
async def private(account=Depends(current_user)):
    return account