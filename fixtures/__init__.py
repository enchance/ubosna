from fastapi import FastAPI, APIRouter

from .data import *
from .perms import *
from app import ic
from app.authentication.models.account import Account, Group, Perm




fixturerouter = APIRouter()


async def insert_groups_and_perms():
    # Groups
    ll = []
    for i in groups:
        ll.append(Group(name=i))
    await Group.bulk_create(ll)
    


@fixturerouter.get('/init', summary='Initial data for the site')
async def init():
    # Groups
    await insert_groups_and_perms()
    # Perms
    # Users
    

@fixturerouter.get('/trades', summary='Trades fixtures')
async def trades_init():
    pass