"""
Ticker business logic service.

This module contains the business logic for ticker operations.
"""

from app.models.ticker import TickerResponse


class TickerService:
    """Service class for ticker-related business logic."""
    
    def get_ticker_data(self) -> TickerResponse:
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
