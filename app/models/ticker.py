"""
Ticker data models.
"""

from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class TickerResponse(BaseModel):
    """Response model for ticker endpoint."""
    symbol: str
    price: float
    message: str

class HistoryResponse(BaseModel):
    """Response model for ticker endpoint."""
    symbol: str
    from_time: datetime
    to_time: datetime

class Underlying(Enum):
    NIFTY = "NIFTY"
    SENSEX = "SENSEX"

class OptionType(Enum):
    CALL = "CE"
    PUT = "PE"
   