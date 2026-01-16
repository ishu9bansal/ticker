"""
Ticker-related endpoints.

Business logic endpoints for ticker functionality.
"""

from fastapi import APIRouter, Depends, Request
from app.api.auth import authenticate_request
from app.services.ticker_service import TickerService

router = APIRouter(dependencies=[Depends(authenticate_request)])
service = TickerService()

@router.get("/instruments")
def instruments():
    try:
        return service.instruments()
    except Exception as e:
        return {"error": str(e)}
    
@router.get("/user")
def user():
    try:
        return service.user()
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
