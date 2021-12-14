from pydantic import BaseModel
from .choices import ActionChoices




class TransactPM(BaseModel):
    action: str
    price: float
    basecurr: str
    quotecurr: str
    fee: float


class TradeCryptoPM(TransactPM):
    pass

# class BuyTradePM(TradePM):
#     action: str = 'buy'
#     buyfees: float
#
# class SellTradePM(TradePM):
#     action: str = 'sell'
#     sellfees: float
