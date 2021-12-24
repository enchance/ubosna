import pytest
from typing import List
from tortoise.query_utils import Prefetch

from app import ic
from app.auth import Account, Group, Perm, Option
from fixtures.data import options_dict



async def check_account_options(accounts: List[Account]):
    """Accounts must have all template options"""
    for i in accounts:
        template_keys = options_dict['template'].keys()
        assert len(i.accountoptions) == len(template_keys)  # noqa
        ll = []
        for opt in i.accountoptions:                            # noqa
            ll.append(opt.name)
        assert not len(set(ll) ^ set(template_keys))

# @pytest.mark.focus
def test_accounts(loop, tempdb):
    async def ab():
        verified_account = await tempdb()
        accounts = await Account.all().prefetch_related(
            Prefetch('accountoptions', queryset=Option.all())
        )
        await check_account_options(accounts)
        
    loop.run_until_complete(ab())
    return

