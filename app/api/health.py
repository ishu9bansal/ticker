"""
Health check endpoints.

These endpoints are used for monitoring and health checks.
"""

from fastapi import APIRouter
from app.models.health import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check():
    """
    Health check endpoint for monitoring service status.
    
    Returns:
        HealthResponse: Current health status of the service
    """
    return HealthResponse(status="healthy")
