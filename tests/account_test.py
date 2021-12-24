import pytest
from typing import List
from tortoise.query_utils import Prefetch

from app import ic, settings as s
from app.auth import Account, Group, Perm, Option
from trades import Broker
from . import account_fn as acct



# @pytest.mark.focus
def test_accounts(loop, tempdb):
    async def ab():
        verified_account = await tempdb()
        accounts = await Account.all().prefetch_related(
            # Only supports `only()` when prefetching
            Prefetch('accountoptions', queryset=Option.all().only('account_id', 'name'),
                     to_attr='options'),
            Prefetch('groups', queryset=Group.all().only('id', 'name')),
            Prefetch('perms', queryset=Perm.all().only('id', 'code')),
            Prefetch('brokers', queryset=Broker.all().only('id', 'name')),
        )
        
        await acct.account_cache(accounts)
        await acct.account_groups(accounts)
        
        if s.ENABLE_LOCAL_TESTS:
            await acct.local_account_options(accounts)
            await acct.local_account_groups(accounts)
        
    loop.run_until_complete(ab())

