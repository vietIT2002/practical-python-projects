"""Data access for links. All queries are parameterised by SQLAlchemy."""

from __future__ import annotations

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from .models import Link


class LinkRepository:
    """Encapsulates database operations for :class:`Link`."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def exists(self, code: str) -> bool:
        return (
            self._session.scalar(select(Link.id).where(Link.code == code)) is not None
        )

    def get_by_code(self, code: str) -> Link | None:
        return self._session.scalar(select(Link).where(Link.code == code))

    def add(self, link: Link) -> None:
        self._session.add(link)

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()

    def increment_clicks(self, code: str) -> None:
        """Increment a link's click count atomically in a single statement."""
        self._session.execute(
            update(Link).where(Link.code == code).values(clicks=Link.clicks + 1)
        )
        self._session.commit()
