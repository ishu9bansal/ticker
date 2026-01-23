"""
Database package setup for SQLAlchemy + Postgres.

This package exposes the SQLAlchemy `engine`, `SessionLocal`,
`get_db` dependency, and base `Base` model class.
"""

from .engine import engine, SessionLocal
from .session import get_db
from .base import Base
