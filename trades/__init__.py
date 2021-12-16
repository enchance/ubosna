from typing import Optional, Union
from tortoise.exceptions import DoesNotExist

from .settings import *
from .pydantic import *
from .choices import *
from .models import *
from app import red
from app.auth import Account, Taxo


tradesettings = TradeSettings()


# async def get_quotecurr(tradetype: str) -> str:
#     if tradetype == TradeChoices.crypto:
#         return tradesettings.QUOTECURR_CRYPTO
#     elif tradetype == TradeChoices.stock:
#         return tradesettings.QUOTECURR_STOCK
#
#
# async def get_broker(account) -> Broker:
#     # INCOMPLETE: Work in progress...
#     pass



async def get_pool(account: Account, currency: str) -> Pool:
    """
    Get the pool for a currency or create a new empty one.
    :param account:     The account which will be using it
    :param currency:    Ticker name
    :return:            Pool
    """
    try:
        pool = await Pool.get(account=account, currency=currency).only('id')
    except DoesNotExist:
        d = {
            'currency': currency,
            'amount': 0,
            'costave': 0,
            'account': account
        }
        pool = await Pool.create(**d)
    return pool


# async def get_exchange(account: Account) -> Taxo:
#     # Check cache if there is a default exchange
#     # If missing, query the db
#     # Reload cache
#     partialkey = tradesettings.CACHE_EXCHANGE.format(account.id)
#     if red.exists(partialkey):
#         exchange_id = int(red.get(partialkey))
#
#     else:
#         try:
#         except DoesNotExist as e:
#             pass
#     return exchange
    
    
    