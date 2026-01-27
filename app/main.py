"""
Main FastAPI application entry point.

This module creates and configures the FastAPI application instance.
All routes from different routers are included here.
"""

from contextlib import asynccontextmanager
import time
from fastapi import FastAPI, Request, logger
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

WARNING_THRESHOLD = 2.0  # 2 second
ERROR_THRESHOLD = 4.0    # 4 seconds
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    Middleware to time API requests and add the duration to a response header.
    """
    start_time = time.perf_counter()  # Use perf_counter for better precision
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    msg = f"Request processed in {process_time:.4f} seconds"
    if process_time > ERROR_THRESHOLD:
        logger.logger.error(msg)
    elif process_time > WARNING_THRESHOLD:
        logger.logger.warning(msg)
    else:
        logger.logger.info(msg) # Log the time
    return response

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
