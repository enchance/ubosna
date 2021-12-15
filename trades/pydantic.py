from typing import List, Optional
from pydantic import BaseModel

from . import get_quotecurr
from .choices import ActionChoices, TradeChoices
from .models import Pool, Broker
from app.auth import Account, Taxo



class TradePM(BaseModel):
    price: float
    basecurr: str
    
    buyamount: float
    storeamount: float
    gross: float
    feesmain: float
    feescurr: str
    total: float
    leverage: Optional[int] = None
    
    status: str = 'ongoing'
    note: str = ''
    
    pool: Pool
    broker: Broker
    exchange: str
    
    is_closed: bool = False
    account: Account
    metadata: dict = {}
    
    tags: Optional[List[Taxo]] = None


class BuyCryptoPM(TradePM):
    action: str = ActionChoices.buy
    quotecurr: str = get_quotecurr()['crypto']
    tradetype: str = TradeChoices.crypto


class BuyStockPM(TradePM):
    action: str = ActionChoices.buy
    quotecurr: str = get_quotecurr()['stock']
    tradetype: str = TradeChoices.stock


class BuyForexPM(TradePM):
    action: str = ActionChoices.buy
    quotecurr: str = get_quotecurr()['forex']
    tradetype: str = TradeChoices.forex


class SellCryptoPM(TradePM):
    action: str = ActionChoices.sell
    quotecurr: str = get_quotecurr()['crypto']
    tradetype: str = TradeChoices.crypto


class SellStockPM(TradePM):
    action: str = ActionChoices.sell
    quotecurr: str = get_quotecurr()['stock']
    tradetype: str = TradeChoices.stock


class SellForexPM(TradePM):
    action: str = ActionChoices.sell
    quotecurr: str = get_quotecurr()['forex']
    tradetype: str = TradeChoices.forex
