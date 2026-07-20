"""FastAPI dependencies for database sessions and the link service."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from ..application.service import LinkService
from ..infrastructure.repository import LinkRepository


def get_session(request: Request) -> Iterator[Session]:
    """Yield a database session bound to the app's engine, closing it after use."""
    session_factory = request.app.state.session_factory
    session: Session = session_factory()
    try:
        yield session
    finally:
        session.close()


SessionDep = Annotated[Session, Depends(get_session)]


def get_service(request: Request, session: SessionDep) -> LinkService:
    settings = request.app.state.settings
    return LinkService(LinkRepository(session), settings.code_length)


ServiceDep = Annotated[LinkService, Depends(get_service)]
