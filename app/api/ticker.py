"""
Ticker-related endpoints.

Business logic endpoints for ticker functionality.
"""

from fastapi import APIRouter, Request
from app.models.ticker import HistoryResponse, TickerResponse
from app.services.ticker_service import TickerService

router = APIRouter()
service = TickerService()


@router.get("/instruments")
def instruments():
    try:
        return service.instruments()
    except Exception as e:
        return {"error": str(e)}

@router.get("/quote")
def quote(req: Request):
    # parse query params
    underlying = req.query_params.get("underlying")
    try:
        return service.quote(underlying)
    except Exception as e:
        return {"error": str(e)}

@router.get("/history")
def history(req: Request):
    underlying = req.query_params.get("underlying")
    from_date = req.query_params.get("from")
    try:
        return service.history(underlying, from_date)
    except Exception as e:
        return {"error": str(e)}
