"""Service-layer tests using a real session against a temporary database."""

from __future__ import annotations

import pytest
from sqlalchemy.orm import Session

from url_shortener.application import codes
from url_shortener.application import service as service_module
from url_shortener.application.service import LinkService
from url_shortener.domain.errors import CodeGenerationError, LinkNotFoundError
from url_shortener.infrastructure.repository import LinkRepository


def _service(session: Session) -> LinkService:
    return LinkService(LinkRepository(session), code_length=7)


def test_click_count_is_transactional(session: Session) -> None:
    service = _service(session)
    link = service.create_link(url="https://example.com")
    service.redirect(link.code)
    service.redirect(link.code)
    assert service.get_link(link.code).clicks == 2


def test_redirect_missing_raises(session: Session) -> None:
    with pytest.raises(LinkNotFoundError):
        _service(session).redirect("missing")


def test_code_generation_gives_up_on_persistent_collision(
    session: Session, monkeypatch: pytest.MonkeyPatch
) -> None:
    service = _service(session)
    service.create_link(url="https://example.com", alias="taken")
    # Force every generated code to collide with the existing alias.
    monkeypatch.setattr(codes, "generate_code", lambda length: "taken")
    monkeypatch.setattr(service_module, "generate_code", lambda length: "taken")
    with pytest.raises(CodeGenerationError):
        service.create_link(url="https://example.com/other")
