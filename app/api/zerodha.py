"""
Zerodha-related endpoints.

Business logic endpoints for zerodha authentication
"""

from fastapi import APIRouter, Depends, HTTPException
from kiteconnect import KiteConnect
from sqlalchemy.orm import Session

from app.api.auth import authenticate_request, get_user
from app.constants import ZERODHA_API_KEY, ZERODHA_API_SECRET
from app.db import get_db
from app.models.clerk import ClerkUser
from app.repository.user_token_repository import UserTokenRepository

kite = KiteConnect(api_key=ZERODHA_API_KEY)
router = APIRouter(dependencies=[Depends(authenticate_request)])

def get_user_id(user: ClerkUser = Depends(get_user)) -> str:
    user_id = user.sub
    if not user_id:
        raise HTTPException(status_code=400, detail="User auth is needed to access TickerService")
    return user_id

@router.post("/")
def registerToken(token: str, db: Session = Depends(get_db), user_id: str = Depends(get_user_id)):
    try:
        repo = UserTokenRepository(db)
        user_token = repo.update_token(user_id, token)
        return {"message": "Token updated successfully", "token": user_token.token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/url")
def getLoginUrl():
    try:
        login_url = kite.login_url()
        return {"login_url": login_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login")
def login(request_token: str, db: Session = Depends(get_db), user_id: str = Depends(get_user_id)):
    try:
        data = kite.generate_session(request_token=request_token, api_secret=ZERODHA_API_SECRET)
        if not data and not data["access_token"]:   # type: ignore
            print(data)
            raise HTTPException(status_code=400, detail="Failed to generate session with provided request token")
        access_token: str = data["access_token"]    # type: ignore
        repo = UserTokenRepository(db)
        repo.update_token(user_id, access_token)
        return {"message": "Logged in successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/logout")
def logout(db: Session = Depends(get_db), user_id: str = Depends(get_user_id)):
    try:
        repo = UserTokenRepository(db)
        token = repo.get_token(user_id)
        kite.invalidate_access_token(token)
        repo.update_token(user_id, "")
        return {"message": "Logged out successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
