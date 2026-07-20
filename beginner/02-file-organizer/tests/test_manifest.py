"""Tests for manifest serialisation."""

from __future__ import annotations

from pathlib import Path

import pytest

from file_organizer.errors import ManifestError
from file_organizer.manifest import load_manifest, save_manifest
from file_organizer.models import Move


def test_save_then_load_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "manifest.json"
    moves = (
        Move(
            tmp_path / "src" / "a.jpg", tmp_path / "dst" / "images" / "a.jpg", "images"
        ),
    )
    save_manifest(path, moves)
    loaded = load_manifest(path)
    assert loaded == list(moves)


def test_load_missing_manifest(tmp_path: Path) -> None:
    with pytest.raises(ManifestError, match="not found"):
        load_manifest(tmp_path / "nope.json")


def test_load_invalid_json(tmp_path: Path) -> None:
    path = tmp_path / "manifest.json"
    path.write_text("{ not json", encoding="utf-8")
    with pytest.raises(ManifestError, match="not valid JSON"):
        load_manifest(path)


def test_load_without_moves_key(tmp_path: Path) -> None:
    path = tmp_path / "manifest.json"
    path.write_text('{"version": 1}', encoding="utf-8")
    with pytest.raises(ManifestError, match="not a valid manifest"):
        load_manifest(path)


def test_load_malformed_entry(tmp_path: Path) -> None:
    path = tmp_path / "manifest.json"
    path.write_text('{"moves": [{"source": "a"}]}', encoding="utf-8")
    with pytest.raises(ManifestError, match="malformed move entry"):
        load_manifest(path)
