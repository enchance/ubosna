from pydantic import BaseSettings



class TradeSettings(BaseSettings):
    BASEQUOTE_CRYPTO: str = 'USDT'
    BASEQUOTE_STOCK: str = 'USD'
    BASEQUOTE_FOREX: str = 'USD'
