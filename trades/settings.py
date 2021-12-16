from pydantic import BaseSettings



class TradeSettings(BaseSettings):
    # Replace this with db soon
    QUOTECURR_CRYPTO: str = 'USDT'
    QUOTECURR_STOCK: str = 'USD'

    # Cache
    CACHE_EXCHANGE: str = 'exchange-{}'
    CACHE_BROKER: str = 'broker-{}'
    
    
tradesettings = TradeSettings()