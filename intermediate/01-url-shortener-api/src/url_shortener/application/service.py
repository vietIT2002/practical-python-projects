"""Business logic for creating, reading, and redirecting links."""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy.exc import IntegrityError

from ..domain.errors import (
    AliasConflictError,
    CodeGenerationError,
    LinkExpiredError,
    LinkNotFoundError,
)
from ..infrastructure.models import Link
from ..infrastructure.repository import LinkRepository
from .codes import generate_code

_MAX_CODE_ATTEMPTS = 10


def _as_utc(value: datetime) -> datetime:
    """Treat a naive datetime (as SQLite may return) as UTC."""
    return value if value.tzinfo is not None else value.replace(tzinfo=UTC)


class LinkService:
    """Coordinates link creation, lookup, and redirect counting."""

    def __init__(self, repository: LinkRepository, code_length: int) -> None:
        self._repository = repository
        self._code_length = code_length

    def create_link(
        self,
        *,
        url: str,
        alias: str | None = None,
        expires_at: datetime | None = None,
    ) -> Link:
        code = self._choose_code(alias)
        link = Link(
            code=code,
            url=url,
            clicks=0,
            created_at=datetime.now(UTC),
            expires_at=expires_at,
        )
        self._repository.add(link)
        try:
            self._repository.commit()
        except IntegrityError as exc:
            # A concurrent request claimed the same code between check and commit.
            self._repository.rollback()
            raise AliasConflictError(code) from exc
        return link

    def _choose_code(self, alias: str | None) -> str:
        if alias is not None:
            if self._repository.exists(alias):
                raise AliasConflictError(alias)
            return alias
        for _ in range(_MAX_CODE_ATTEMPTS):
            candidate = generate_code(self._code_length)
            if not self._repository.exists(candidate):
                return candidate
        raise CodeGenerationError("could not generate a unique code")

    def get_link(self, code: str) -> Link:
        link = self._repository.get_by_code(code)
        if link is None:
            raise LinkNotFoundError(code)
        if self._is_expired(link):
            raise LinkExpiredError(code)
        return link

    def redirect(self, code: str) -> str:
        link = self.get_link(code)
        self._repository.increment_clicks(code)
        return link.url

    @staticmethod
    def _is_expired(link: Link) -> bool:
        if link.expires_at is None:
            return False
        return datetime.now(UTC) >= _as_utc(link.expires_at)
