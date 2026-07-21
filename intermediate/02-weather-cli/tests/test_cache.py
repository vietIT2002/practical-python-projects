"""Tests for the TTL file cache (deterministic via an injected clock)."""

from __future__ import annotations

from pathlib import Path

from weather_cli.cache import FileCache


def test_set_then_get_within_ttl(tmp_path: Path) -> None:
    clock = {"t": 1000.0}
    cache = FileCache(tmp_path, ttl_seconds=600, now=lambda: clock["t"])
    cache.set("key", {"value": 1})
    assert cache.get("key") == {"value": 1}


def test_expires_after_ttl(tmp_path: Path) -> None:
    clock = {"t": 1000.0}
    cache = FileCache(tmp_path, ttl_seconds=600, now=lambda: clock["t"])
    cache.set("key", {"value": 1})
    clock["t"] = 1000.0 + 601
    assert cache.get("key") is None


def test_missing_key_returns_none(tmp_path: Path) -> None:
    cache = FileCache(tmp_path, ttl_seconds=600, now=lambda: 0.0)
    assert cache.get("absent") is None


def test_corrupt_entry_returns_none(tmp_path: Path) -> None:
    cache = FileCache(tmp_path, ttl_seconds=600, now=lambda: 0.0)
    cache.set("key", {"value": 1})
    # Corrupt the stored file.
    stored = next(tmp_path.glob("*.json"))
    stored.write_text("not json", encoding="utf-8")
    assert cache.get("key") is None
