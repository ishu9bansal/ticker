from __future__ import annotations

from typing import Generic, Iterable, Optional, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session


T = TypeVar("T")


class RepositoryBase(Generic[T]):
    def __init__(self, session: Session, model_type: type[T]):
        self.session = session
        self.model_type = model_type

    def add(self, instance: T) -> T:
        self.session.add(instance)
        return instance

    def add_all(self, instances: Iterable[T]) -> Iterable[T]:
        self.session.add_all(list(instances))
        return instances

    def get(self, id: int) -> Optional[T]:
        return self.session.get(self.model_type, id)

    def list(self, limit: int | None = None) -> list[T]:
        stmt = select(self.model_type)
        if limit:
            stmt = stmt.limit(limit)
        return list(self.session.execute(stmt).scalars().all())

    def delete(self, instance: T) -> None:
        self.session.delete(instance)
