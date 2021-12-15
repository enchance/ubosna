from enum import IntEnum, Enum



class ActionChoices(IntEnum):
    buy = 1
    sell = 2
    
    
class TradeChoices(Enum):
    crypto = 'crypto'
    stock = 'stock'
    forex = 'forex'
