"""
Ticker business logic service.

This module contains the business logic for ticker operations.
"""

from datetime import datetime
from app.brokers.zerodha import Broker, Underlying


class TickerService:
    """Service class for ticker-related business logic."""
    def __init__(self) -> None:
        self.broker = Broker()
    
    def instruments(self):
        return self.broker.instruments()
    
    def quote(self, underlying_str: str | None):
        if not underlying_str:
            raise ValueError("Underlying parameter is required")
        u = Underlying(underlying_str)
        return self.broker.quote(self.broker.findStock(u))
    
    def history(self, underlying_str: str | None, from_str: str | None):
        if not underlying_str:
            raise ValueError("Underlying parameter is required")
        if not from_str:
            raise ValueError("From parameter is required, in datetime format YYYY-MM-DDTHH:mm:ss")
        from_date = datetime.fromisoformat(from_str)
        to_date = datetime.now()
        u = Underlying(underlying_str)
        stock_instrument = self.broker.findStock(u)
        return self.broker.history(stock_instrument, from_date, to_date)

