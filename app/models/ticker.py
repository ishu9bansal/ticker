"""
Ticker data models.
"""

from datetime import datetime
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
