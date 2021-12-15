from typing import List, Optional, Any
from pydantic import BaseModel

from .choices import StatusChoices


class TradePM(BaseModel):
    # User input
    action: str
    price: float
    amount: float
    basecurr: str
    quotecurr: str
    note: str = ''
    account: Any
    exchange: Optional[Any]
    broker: Optional[Any]
    tags: Optional[List[Any]]
    leverage: Optional[int]

    # Computed
    storeamount: float = 0
    gross: float = 0
    feesmain: float = 0
    feescurr: str = ''
    total: float = 0
    tradetype: str = ''
    status: int = StatusChoices.ongoing
    is_closed: bool = False
    metadata: dict = {}
