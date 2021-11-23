import random
from fastapi import FastAPI, APIRouter, Depends, Query
from tortoise.transactions import atomic
from pydantic import EmailStr, ValidationError

from .data import *
from .perms import *
from app import ic
from app.auth import create_user
from app.authentication.models.account import Account, Group, Perm, GroupPerms
from app.authentication.models.pydantic import UserCreate




fixturerouter = APIRouter()


async def insert_groups_and_perms():
    """Insert groups, perms, and group perms."""
    success = []
    
    # Groups
    ll = []
    for i in perm_init:
        ll.append(Group(name=i))
    await Group.bulk_create(ll)
    success.append('Groups created.')

    # Perms
    ss = set()
    for groupname, val in perm_init.items():
        for k, v in val.items():
            ss.update({f'{k}.{i}' for i in v})
    ll = []
    for i in sorted(ss):
        ll.append(Perm(code=i))
    await Perm.bulk_create(ll)
    success.append('Perms created')
    
    # Group x Perm
    group_dict = dict(await Group.all().values_list('name', 'id'))
    perm_dict = dict(await Perm.all().values_list('code', 'id'))
    
    ll = []
    for group, group_id in group_dict.items():
        for k, v in perm_init[group].items():
            for i in v:
                perm_id = perm_dict[f'{k}.{i}']
                ll.append(GroupPerms(group_id=group_id, perm_id=perm_id))
    await GroupPerms.bulk_create(ll)
    success.append('Group x Perms created.')
    
    return success


async def insert_accounts():
    """Create users."""
    with open('/usr/share/dict/cracklib-small', 'r') as w:
        words = w.read().splitlines()
        
    verified_list = []
    total = 0
    verified = 5
    unverified = 4
    superemails = ['super1@gmail.com', 'super2@gmail.com']
    password = 'pass123'
    
    def random_email(words: list):
        word = random.choice(words)
        tld = random.choice(['org', 'com', 'net', 'io', 'com.ph', 'co.uk'])
        return f'{word}@{word}.{tld}'

    try:
        # Superuser
        for email in superemails:
            await create_user(email, password, is_superuser=True)
            total += 1
        await Account.filter(email__in=superemails).update(is_verified=True)
        
        # Verified
        ll = ['verified@gmail.com']
        for _ in range(verified):
            ll.append(random_email(words))
        for email in ll:
            await create_user(email, password)
            verified_list.append(email)
            total += 1
        await Account.filter(email__in=verified_list).update(is_verified=True)

        # Unverified
        ll = ['unverified@gmail.com']
        for _ in range(unverified):
            ll.append(random_email(words))
        for email in ll:
            await create_user(email, password)
            total += 1
    except ValidationError:
        pass
        
    return [f'{total} accounts created.']


async def insert_options():
    return []


async def insert_taxos():
    return []


@atomic
@fixturerouter.get('/init', summary='Initial data for the site')
async def init(accounts_only: bool = False, options_only: bool = False, taxos_only: bool = False):
    success = []
    if not accounts_only or not options_only or not taxos_only:
        success += await insert_groups_and_perms()
    if not options_only or not taxos_only:
        success += await insert_accounts()
    if not accounts_only or not taxos_only:
        success += await insert_options()
    if not options_only or not accounts_only:
        success += await insert_taxos()
    return success
    

@fixturerouter.get('/trades', summary='Trades fixtures')
async def trades_init():
    pass