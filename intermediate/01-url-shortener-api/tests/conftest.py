"""Shared fixtures: an isolated temporary database per test."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from url_shortener.infrastructure.db import Base, build_engine, build_session_factory
from url_shortener.main import create_app
from url_shortener.settings import Settings


def _settings(tmp_path: Path) -> Settings:
    return Settings(
        database_url=f"sqlite:///{tmp_path / 'test.db'}",
        base_url="http://testserver",
    )


@pytest.fixture
def client(tmp_path: Path) -> Iterator[TestClient]:
    app = create_app(_settings(tmp_path))
    Base.metadata.create_all(app.state.engine)
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def session(tmp_path: Path) -> Iterator[Session]:
    engine = build_engine(f"sqlite:///{tmp_path / 'svc.db'}")
    Base.metadata.create_all(engine)
    factory = build_session_factory(engine)
    db_session = factory()
    try:
        yield db_session
    finally:
        db_session.close()
