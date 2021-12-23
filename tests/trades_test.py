import pytest

from app import ic


@pytest.mark.focus
def test_make_trade(loop, tempdb):
    async def ab():
        await tempdb()
    #     # verified_account = await tempdb()
    #     # ic(verified_account)
        return 'foo'
    
    loop.run_until_complete(ab())