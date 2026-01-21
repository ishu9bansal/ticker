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

@router.get("/straddles")
def straddles(req: Request):
    # parse query params
    underlying = req.query_params.get("underlying")
    try:
        return service.straddles(underlying)
    except Exception as e:
        return {"error": str(e)}

@router.get("/straddleQuotes")
def straddleQuotes(req: Request):
    # parse query params
    ids = req.query_params.get("ids")
    idList = ids.split(",") if ids else []
    try:
        return service.straddle_quotes(idList)
    except Exception as e:
        return {"error": str(e)}

@router.get("/history")
def history(req: Request):
    underlying = req.query_params.get("underlying")
    from_date = req.query_params.get("from")
    to_date = req.query_params.get("to")
    try:
        return service.history(underlying, from_date, to_date)
    except Exception as e:
        return {"error": str(e)}

@router.get("/straddleHistory")
def historyStraddle(req: Request):
    straddleId = req.query_params.get("straddle")
    from_date = req.query_params.get("from")
    to_date = req.query_params.get("to")
    try:
        return service.straddleHistory(straddleId, from_date, to_date)
    except Exception as e:
        return {"error": str(e)}

