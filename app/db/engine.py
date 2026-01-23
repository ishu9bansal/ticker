from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.constants.index import POSTGRES_CONNECTION


def _normalized_url(url: str) -> str:
    if not url:
        return url
    # Prefer psycopg (v3) driver if no explicit driver is provided
    if url.startswith("postgresql://"):
        return "postgresql+psycopg" + url[len("postgresql"):]
    return url


if not POSTGRES_CONNECTION:
    # Provide a clear error if connection string is missing at runtime
    # We intentionally don't raise here to avoid import-time failures in non-DB flows.
    # The first DB access will surface a meaningful error.
    pass

engine = create_engine(
    _normalized_url(POSTGRES_CONNECTION),
    pool_pre_ping=True,
)

SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
