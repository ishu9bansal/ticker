"""
Main FastAPI application entry point.

This module creates and configures the FastAPI application instance.
All routes from different routers are included here.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import health, ticker
from app.constants.index import ALLOWED_ORIGINS

# Create FastAPI application instance
app = FastAPI(
    title="Ticker API",
    version="0.1.0",
    description="A simple FastAPI backend project for learning deployment"
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


@app.get("/")
def read_root():
    """
    Root endpoint - Simple Hello World message.
    """
    return {"message": "Hello World", "version": "0.1.0"}
