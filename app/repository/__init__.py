"""
Repository layer for database operations.

This package contains repository classes that implement the data access pattern,
providing a clean abstraction over database models and sessions.
"""

from .base import RepositoryBase
from .price_snapshot_repository import PriceSnapshotRepository

__all__ = [
    "RepositoryBase",
    "PriceSnapshotRepository",
]
