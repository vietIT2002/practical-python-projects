"""End-to-end CLI tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from contact_book.cli import main


def _base(tmp_path: Path) -> list[str]:
    return ["--data-file", str(tmp_path / "contacts.json")]


def test_add_then_list(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    base = _base(tmp_path)
    assert main([*base, "add", "--name", "Ada", "--email", "ada@example.com"]) == 0
    assert "Added contact" in capsys.readouterr().out
    assert main([*base, "list"]) == 0
    assert "Ada" in capsys.readouterr().out


def test_search_and_update_and_delete(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    base = _base(tmp_path)
    main([*base, "add", "--name", "Grace Hopper"])
    contact_id = (
        capsys.readouterr().out.split("Added contact ")[1].split(":")[0].strip()
    )

    assert main([*base, "search", "grace"]) == 0
    assert "Grace" in capsys.readouterr().out

    assert main([*base, "update", contact_id, "--phone", "5551234567"]) == 0
    capsys.readouterr()
    assert main([*base, "search", "5551234567"]) == 0
    assert "Grace" in capsys.readouterr().out

    assert main([*base, "delete", contact_id]) == 0
    assert main([*base, "delete", "missing"]) == 1
    assert "error" in capsys.readouterr().err


def test_add_invalid_returns_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([*_base(tmp_path), "add", "--name", ""]) == 1
    assert "error" in capsys.readouterr().err


def test_export(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    base = _base(tmp_path)
    main([*base, "add", "--name", "Ada"])
    capsys.readouterr()
    out_csv = tmp_path / "out.csv"
    assert main([*base, "export", str(out_csv)]) == 0
    assert out_csv.is_file()
    # Refuses to overwrite without --force.
    assert main([*base, "export", str(out_csv)]) == 1
    assert "error" in capsys.readouterr().err
