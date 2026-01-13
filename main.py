"""
Entry point for the Ticker API application.

This file serves as the entry point and imports the FastAPI app instance
from the app package. This pattern ensures:
1. Clean separation of concerns
2. Proper module imports work both locally and in production
3. The application can be run with: uvicorn main:app

For local development: uvicorn main:app --reload
For production: uvicorn main:app --host 0.0.0.0 --port $PORT
"""

from app.main import app

# The 'app' variable is imported from app.main and will be used by uvicorn
# when you run: uvicorn main:app

__all__ = ["app"]
