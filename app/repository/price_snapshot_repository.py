from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import PriceSnapshot
from .base import RepositoryBase


class PriceSnapshotRepository(RepositoryBase[PriceSnapshot]):
    def __init__(self, session: Session):
        super().__init__(session, PriceSnapshot)

    def by_symbol(self, symbol: str, limit: int | None = None) -> list[PriceSnapshot]:
        stmt = select(PriceSnapshot).where(PriceSnapshot.symbol == symbol).order_by(PriceSnapshot.created_at.desc())
        if limit:
            stmt = stmt.limit(limit)
        return list(self.session.execute(stmt).scalars().all())
