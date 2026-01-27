"""
Ticker-related endpoints.

Business logic endpoints for ticker functionality.
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.api.auth import authenticate_request, get_user
from app.db import get_db
from app.db.models import PriceSnapshot
from app.models.clerk import ClerkUser
from app.repository.price_snapshot_repository import PriceSnapshotRepository
from app.repository.user_token_repository import UserTokenRepository
from app.services.ticker_service import TickerService
from app.utils import timer

router = APIRouter(dependencies=[Depends(authenticate_request)])

@timer
def get_service(user: ClerkUser = Depends(get_user), db: Session = Depends(get_db)) -> TickerService:
    user_id = user.sub
    if not user_id:
        raise HTTPException(status_code=400, detail="User auth is needed to access TickerService")
    repo = UserTokenRepository(db)
    token = repo.get_token(user_id)
    if not token:
        raise HTTPException(status_code=400, detail="User token not found in database")
    return TickerService(token)

@router.get("/instruments")
def instruments(service: TickerService = Depends(get_service)):
    try:
        return service.instruments()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user")
def user(service: TickerService = Depends(get_service)):
    try:
        return service.user()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/quote")
def quote(underlying: str, service: TickerService = Depends(get_service)):
    try:
        return service.quote(underlying)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/straddles")
def straddles(underlying: str, service: TickerService = Depends(get_service)):
    try:
        return service.straddles(underlying)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/straddleQuotes")
def straddleQuotes(ids: str, service: TickerService = Depends(get_service)):
    idList = ids.split(",") if ids else []
    try:
        return service.straddle_quotes(idList)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
def history(req: Request, service: TickerService = Depends(get_service)):
    underlying = req.query_params.get("underlying")
    from_date = req.query_params.get("from")
    to_date = req.query_params.get("to")
    try:
        return service.history(underlying, from_date, to_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/straddleHistory")
def historyStraddle(req: Request, service: TickerService = Depends(get_service)):
    straddleId = req.query_params.get("straddle")
    from_date = req.query_params.get("from")
    to_date = req.query_params.get("to")
    try:
        return service.straddleHistory(straddleId, from_date, to_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# === DB Demo Endpoints ===
# These endpoints demonstrate the repository pattern and database usage.


@router.post("/snapshots")
def create_snapshot(symbol: str, price: float, db: Session = Depends(get_db)):
    """
    Create a new price snapshot in the database.
    
    Args:
        symbol: Ticker symbol (e.g., 'NIFTY', 'SENSEX')
        price: Current price
        db: Database session (injected via dependency)
    
    Returns:
        Created snapshot with ID and timestamp
    """
    try:
        repo = PriceSnapshotRepository(db)
        snapshot = PriceSnapshot(symbol=symbol, price=price)
        repo.add(snapshot)
        db.commit()
        db.refresh(snapshot)
        return {
            "id": snapshot.id,
            "symbol": snapshot.symbol,
            "price": snapshot.price,
            "created_at": snapshot.created_at.isoformat() if snapshot.created_at else None,
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/snapshots/{symbol}")
def list_snapshots(symbol: str, limit: int = 10, db: Session = Depends(get_db)):
    """
    List recent price snapshots for a given symbol.
    
    Args:
        symbol: Ticker symbol to filter by
        limit: Max number of records to return (default: 10)
        db: Database session (injected via dependency)
    
    Returns:
        List of recent price snapshots ordered by creation time (newest first)
    """
    try:
        repo = PriceSnapshotRepository(db)
        snapshots = repo.by_symbol(symbol, limit=limit)
        return [
            {
                "id": snap.id,
                "symbol": snap.symbol,
                "price": snap.price,
                "created_at": snap.created_at.isoformat() if snap.created_at else None,
            }
            for snap in snapshots
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/snapshots")
def all_snapshots(limit: int = 20, db: Session = Depends(get_db)):
    """
    List all price snapshots across all symbols.
    
    Args:
        limit: Max number of records to return (default: 20)
        db: Database session (injected via dependency)
    
    Returns:
        List of all recent price snapshots
    """
    try:
        repo = PriceSnapshotRepository(db)
        snapshots = repo.list(limit=limit)
        return [
            {
                "id": snap.id,
                "symbol": snap.symbol,
                "price": snap.price,
                "created_at": snap.created_at.isoformat() if snap.created_at else None,
            }
            for snap in snapshots
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
