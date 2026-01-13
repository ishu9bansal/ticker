"""
Ticker-related endpoints.

Business logic endpoints for ticker functionality.
"""

from fastapi import APIRouter
from app.models.ticker import TickerResponse
from app.services.ticker_service import TickerService

router = APIRouter()
ticker_service = TickerService()


@router.get("/ticker", response_model=TickerResponse)
def get_ticker():
    """
    Get current ticker information.
    
    Returns:
        TickerResponse: Current ticker data
    """
    return ticker_service.get_ticker_data()
