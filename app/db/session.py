from collections.abc import Generator
from sqlalchemy.orm import Session

from app.utils import timer

from .engine import SessionLocal

@timer
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
