"""
Zerodha-related endpoints.

Business logic endpoints for zerodha authentication
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.auth import authenticate_request, get_user
from app.db import get_db
from app.models.clerk import ClerkUser
from app.repository.user_token_repository import UserTokenRepository

router = APIRouter(dependencies=[Depends(authenticate_request)])

def get_user_id(user: ClerkUser = Depends(get_user)) -> str:
    user_id = user.sub
    if not user_id:
        raise HTTPException(status_code=400, detail="User auth is needed to access TickerService")
    return user_id

@router.post("/")
def instruments(token: str, db: Session = Depends(get_db), user_id: str = Depends(get_user_id)):
    try:
        repo = UserTokenRepository(db)
        user_token = repo.update_token(user_id, token)
        return {"message": "Token updated successfully", "token": user_token.token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
