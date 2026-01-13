"""
Main FastAPI application entry point.

This module creates and configures the FastAPI application instance.
All routes from different routers are included here.
"""

from fastapi import FastAPI
from app.api import health, ticker

# Create FastAPI application instance
app = FastAPI(
    title="Ticker API",
    version="0.1.0",
    description="A simple FastAPI backend project for learning deployment"
)

# Include routers from different modules
app.include_router(health.router, tags=["health"])
app.include_router(ticker.router, prefix='/ticker', tags=["ticker"])


@app.get("/")
def read_root():
    """
    Root endpoint - Simple Hello World message.
    """
    return {"message": "Hello World", "version": "0.1.0"}
