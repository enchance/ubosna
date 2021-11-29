from pydantic import BaseModel




class TradePM(BaseModel):
    base: int
    quote: int
    pool: int
    broker: int
    price: float
    amount: float
    gross: float
    total: float
    tradetype: str

class BuyTradePM(TradePM):
    action: str = 'buy'
    buyfees: float

class SellTradePM(TradePM):
    action: str = 'sell'
    sellfees: float
