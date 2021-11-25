import random
from fastapi import FastAPI, APIRouter, Depends, Query
from tortoise.transactions import atomic
from tortoise.query_utils import Q
from pydantic import EmailStr, ValidationError

from .data import *
from .perms import *
from app import ic, settings as s, red, cache
from app.auth import create_user
from app.authentication.models.account import Account, Group, Perm, GroupPerms
from app.authentication.models.common import Option, Taxo
from app.authentication.models.pydantic import UserCreate
from app.pydantic import OptionTemplate




fixturerouter = APIRouter()


async def insert_groups():
    # Check for existing
    groupnames = list(perm_init.keys())
    grouplist = await Group.filter(name__in=groupnames).values_list('name', flat=True)
    
    ll = []
    for i in perm_init:
        if i not in grouplist:
            ll.append(Group(name=i))
    await Group.bulk_create(ll)
    
    # Caching for this is done in Group.get_and_cache()
    return ['Groups created.']

    
async def insert_perms():
    """Insert groups, perms, and group perms."""
    success = []

    # Check for existing
    permlist = await Perm.all().values_list('code', flat=True)

    # Perms
    ss = set()
    for groupname, val in perm_init.items():
        for k, v in val.items():
            ss.update({f'{k}.{i}' for i in v})
    ll = []
    for i in sorted(ss):
        if i not in permlist:
            ll.append(Perm(code=i))
    await Perm.bulk_create(ll)
    success.append('Perms created.')
    
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
    
    # CACHE
    for group, _ in group_dict.items():
        await Group.get_and_cache(group)
    
    success.append('Group x Perms created.')
    
    return success


async def insert_accounts(*, verified: int, unverified: int):
    """Create users."""
    with open('/usr/share/dict/cracklib-small', 'r') as w:
        words = w.read().splitlines()
        
    verified_list = []
    total = 0
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
            
        # Options
        opt_templates = await Option.get_templates()
        new_accounts = await Account.filter(Q(account_options=None))\
            .values_list('id', flat=True)
        
        ll = []
        for id in new_accounts:
            for k, v in (opt_templates.dict()).items():
                ll.append(Option(name=k, value=v, optiontype='account', account_id=id))
        await Option.bulk_create(ll)
        
    except ValidationError:
        pass
        
    return [f'{total} accounts created.']


async def insert_options():
    optdb = await Option.all().values_list('name', flat=True)
    
    ll = []
    for optiontype, val in options_dict.items():
        for k, v in val.items():
            # Prevent multiple inserts
            if k in optdb:
                continue
            ll.append(Option(name=k, value=v, optiontype=optiontype))
    ll and await Option.bulk_create(ll)
    
    # Cache
    partialkey = s.CACHE_OPTION_SITE
    red.set(partialkey, cache.makesafe_dict(options_dict['site']), clear=True)
    partialkey = s.CACHE_OPTION_ADMIN
    red.set(partialkey, cache.makesafe_dict(options_dict['admin']), clear=True)
    partialkey = s.CACHE_OPTION_TEMPLATE
    red.set(partialkey, cache.makesafe_dict(options_dict['template']), clear=True)
    
    return ['Options created.']


async def insert_taxos():
    taxodb = await Taxo.filter(taxotype='tag').values_list('name', flat=True)
    
    ll = []
    for tag in taxos_dict['global']['tags']:
        # Prevent multiple inserts
        if tag in taxodb:
            continue
        ll.append(Taxo(name=tag, taxotype='tag', is_global=True))
    ll and await Taxo.bulk_create(ll)
    
    # Cache
    partialkey = s.CACHE_TAXO_TAG_TEMPLATE
    red.set(partialkey, taxos_dict['global']['tags'], clear=True)
    
    return ['Taxos created.']


@atomic
@fixturerouter.get('/init', summary='Initial data for the site')
async def init(
        verified: int = 4, unverified: int = 3,
        accounts: bool = True, groups: bool = True, perms: bool = True,
        options: bool = True, taxos: bool = True
):
    success = []
    if groups:
        success += await insert_groups()
    if perms:
        success += await insert_perms()
    if options:
        # Must come before accounts
        success += await insert_options()
    if taxos:
        # Must come before accounts
        success += await insert_taxos()
    if accounts:
        success += await insert_accounts(verified=verified, unverified=unverified)
    return success
    

@fixturerouter.get('/trades', summary='Trades fixtures')
async def trades_init():
    pass