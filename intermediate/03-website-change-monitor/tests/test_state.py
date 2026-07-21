"""Tests for state persistence."""

from __future__ import annotations

from pathlib import Path

import pytest

from website_change_monitor.errors import StateError
from website_change_monitor.state import load_state, save_state


def test_missing_state_is_empty(tmp_path: Path) -> None:
    assert load_state(tmp_path / "none.json") == {}


def test_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "state.json"
    state = {"https://example.com": {"hash": "abc", "excerpt": "hi", "checked_at": "t"}}
    save_state(path, state)
    assert load_state(path) == state


def test_invalid_json(tmp_path: Path) -> None:
    path = tmp_path / "state.json"
    path.write_text("{ not json", encoding="utf-8")
    with pytest.raises(StateError, match="not valid JSON"):
        load_state(path)


def test_non_object(tmp_path: Path) -> None:
    path = tmp_path / "state.json"
    path.write_text("[]", encoding="utf-8")
    with pytest.raises(StateError, match="must contain an object"):
        load_state(path)
