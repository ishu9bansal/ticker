"""
Ticker business logic service.

This module contains the business logic for ticker operations.
"""

from datetime import datetime
from app.models.ticker import HistoryResponse, TickerResponse


class TickerService:
    """Service class for ticker-related business logic."""
    
    def instruments(self) -> TickerResponse:
        """
        Get ticker data.
        
        In a real application, this would fetch data from a database or external API.
        
        Returns:
            TickerResponse: Ticker data
        """
        return TickerResponse(
            symbol="DEMO",
            price=100.50,
            message="This is example ticker data"
        )
    
    def quote(self, underlying_str: str | None) -> TickerResponse:
        if not underlying_str:
            raise ValueError("Underlying parameter is required")
        return TickerResponse(
            symbol=underlying_str,
            price=590,
            message="No message"
        )
    
    def history(self, underlying_str: str | None, from_str: str | None) -> HistoryResponse:
        if not underlying_str:
            raise ValueError("Underlying parameter is required")
        if not from_str:
            raise ValueError("From parameter is required, in datetime format YYYY-MM-DDTHH:mm:ss")
        from_date = datetime.fromisoformat(from_str)
        return HistoryResponse(
            symbol=underlying_str,
            from_time=from_date,
            to_time=datetime.now()
        )
    
    
