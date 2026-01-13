"""
Ticker data models.
"""

from pydantic import BaseModel


class TickerResponse(BaseModel):
    """Response model for ticker endpoint."""
    symbol: str
    price: float
    message: str
