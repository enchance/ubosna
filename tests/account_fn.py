from typing import List

from app import settings as s, ic
from app.auth import Account, Group, Perm, AccountGroups
from fixtures.data import options_dict



async def local_account_options(accounts: List[Account]):
    """Accounts must have all template options. Relies on fixin/data.py"""
    for i in accounts:
        option_keys = options_dict['template'].keys()
        assert len(i.options) == len(option_keys)                        # noqa
        ss = set()
        for opt in i.options:                                            # noqa
            ss.add(opt.name)
        assert not len(ss ^ set(option_keys))

async def local_account_groups(accounts: List[Account]):
    for account in accounts:
        groups = account.groups
        nameset = {i.name for i in groups}
        assert not nameset ^ set(s.USER_GROUPS)

async def account_cache(accounts: List[Account]):
    for account in accounts:
        # ic(account.id)
        # ic(await account.get_cache('groups'))
        # ic(await account.get_groups())
        
        # ic(groups)
        # ic(account.id)
        # g = await AccountGroups.filter(account_id=account.id).prefetch_related('group')
        # for i in g:
        #     ic(i.group.name)
        pass

async def account_groups(accounts: List[Account]):
    for account in accounts:
        groupnames = [i.name for i in account.groups]
        
        # Get groups
        # ic(await account.get_cache('groups'))
        names, cached = await account.get_groups(dev=True)
        assert not cached
        names, cached = await account.get_groups(dev=True)
        assert cached
        assert not set(names) ^ set(groupnames)
        
        # Add group
        # Get group
        # Cache

async def local_account_perms(accounts: List[Account]):
    # List of default perms
    pass

