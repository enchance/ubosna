from typing import Optional, Union

from app.auth import Taxo
from .models import Broker
from .choices import TradeChoices
from .settings import TradeSettings


tsettings = TradeSettings()


async def get_quotecurr(tradetype: str) -> str:
    # INCOMPLETE: Work in progress...
    if tradetype == TradeChoices.crypto:
        return tsettings.BASEQUOTE_CRYPTO
    elif tradetype == TradeChoices.stock:
        return tsettings.BASEQUOTE_STOCK
    elif tradetype == TradeChoices.forex:
        return tsettings.BASEQUOTE_FOREX


# TODO: Importing these causes import errors. Find out why.

# async def get_broker(account) -> Broker:
#     # INCOMPLETE: Work in progress...
#     pass
#
# async def get_exchange(account) -> Taxo:
#     # INCOMPLETE: Work in progress...
#     pass