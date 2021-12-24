import pytest
from typing import List
from tortoise.query_utils import Prefetch

from app import ic, settings as s
from app.auth import Account, Group, Perm, Option
from trades import Broker
from . import account_fn as acct
from fixtures.data import *


@pytest.mark.usefixtures('accounts')
class TestAccount:

    # @pytest.mark.focus
    def test_accounts(self, loop):
        # ic(self.accounts)
        # async def ab():
        #     await acct.account_cache(accounts)
        #     await acct.account_groups(accounts)
        #
        #     if s.ENABLE_LOCAL_TESTS:
        #         await acct.local_account_options(accounts)
        #         await acct.local_account_groups(accounts)
        #
        # loop.run_until_complete(ab())
        pass
    
    def test_account_groups(self, loop):
        async def ab():
            # ic(self.accounts)
            for account in self.accounts:
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
        loop.run_until_complete(ab())
    
    def test_local_account_options(self, loop):
        """Accounts must have all template options. Relies on fixin/data.py"""
        if s.ENABLE_LOCAL_TESTS:
            async def ab():
                # ic(self.accounts)
                for i in self.accounts:
                    option_keys = options_dict['template'].keys()
                    assert len(i.options) == len(option_keys)                        # noqa
                    ss = set()
                    for opt in i.options:                                            # noqa
                        ss.add(opt.name)
                    assert not len(ss ^ set(option_keys))
            loop.run_until_complete(ab())
    
    def test_local_account_groups(self, loop):
        if s.ENABLE_LOCAL_TESTS:
            async def ab():
                for account in self.accounts:
                    groups = account.groups
                    nameset = {i.name for i in groups}
                    assert not nameset ^ set(s.USER_GROUPS)
            loop.run_until_complete(ab())
            
            
@pytest.mark.usefixtures('accounts')
class TestFoo:
    def test_bar(self, loop):
        async def ab():
            # ic(self.accounts)
            pass
        loop.run_until_complete(ab())
