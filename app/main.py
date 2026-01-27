"""
Main FastAPI application entry point.

This module creates and configures the FastAPI application instance.
All routes from different routers are included here.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import health, ticker, zerodha
from app.constants.index import ALLOWED_ORIGINS
from app.db import Base, engine, SessionLocal
from sqlalchemy import text

# Create FastAPI application instance
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables and test connection
    try:
        Base.metadata.create_all(bind=engine)
        # quick connectivity check
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as e:
        # Defer raising; app can still run without DB for non-DB routes
        # but log the error so it's visible in server output.
        print(f"[DB] Startup check failed: {e}")
    yield
    # Shutdown: remove session scope
    try:
        SessionLocal.remove()
    except Exception:
        pass


app = FastAPI(
    title="Ticker API",
    version="0.1.0",
    description="A simple FastAPI backend project for learning deployment",
    lifespan=lifespan,
)

# Configure CORS - Get allowed origins from environment variable
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers from different modules
app.include_router(health.router, tags=["health"])
app.include_router(ticker.router, prefix='/ticker', tags=["ticker"])
app.include_router(zerodha.router, prefix='/zerodha', tags=["zerodha"])


@app.get("/")
def read_root():
    """
    Root endpoint - Simple Hello World message.
    """
    return {"message": "Hello World", "version": "0.1.0"}
