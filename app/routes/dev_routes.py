from typing import Optional, Union
from fastapi import APIRouter, Response, Query, Path, Depends
from tortoise.query_utils import Prefetch

from app import settings as s
from app.authentication.models.account import Group, Perm, Account


devrouter = APIRouter()

@devrouter.get('/')
async def index(_: Response):
    id = '39af25ef-0bda-4118-a6a7-7b40216cec61'
    account = await Account.get(id=id)
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
    # dbperms = await Perm.filter(perm_groups__name__in=['AccountGroup'])\
    #     .values_list('code', flat=True)
    # return dbperms
    # perms = await Perm.get_perms('AccountGroup', 'ModGroupSet')
    # return perms

    # return await Group.filter(name__in={'AccountGroup', 'TradeGroup'}).only('id', 'name')
    
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