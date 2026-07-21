"""CLI tests with HTTP mocked (no real network)."""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path

import httpx
import pytest

from website_change_monitor import cli

Serve = Callable[..., None]


@pytest.fixture
def serve(monkeypatch: pytest.MonkeyPatch) -> Serve:
    def install(body: str = "<p>hello</p>", status: int = 200) -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(
                status, headers={"content-type": "text/html"}, content=body.encode()
            )

        monkeypatch.setattr(
            cli,
            "create_http_client",
            lambda: httpx.Client(transport=httpx.MockTransport(handler)),
        )

    return install


def test_change_then_unchanged_exit_codes(
    serve: Serve, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    state_file = tmp_path / "state.json"
    serve(body="<p>v1</p>")
    assert cli.main(["https://example.com", "--state-file", str(state_file)]) == 10
    capsys.readouterr()
    assert cli.main(["https://example.com", "--state-file", str(state_file)]) == 0


def test_failed_check_exit_code(serve: Serve, tmp_path: Path) -> None:
    serve(status=500)
    code = cli.main(["https://example.com", "--state-file", str(tmp_path / "s.json")])
    assert code == 20


def test_no_urls_is_usage_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert cli.main(["--state-file", str(tmp_path / "s.json")]) == 2
    assert "error" in capsys.readouterr().err


def test_config_file_urls(serve: Serve, tmp_path: Path) -> None:
    serve(body="<p>x</p>")
    config = tmp_path / "config.json"
    config.write_text(json.dumps({"urls": ["https://example.com"]}), encoding="utf-8")
    code = cli.main(["--config", str(config), "--state-file", str(tmp_path / "s.json")])
    assert code == 10


def test_invalid_config_is_usage_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    config = tmp_path / "config.json"
    config.write_text("[]", encoding="utf-8")
    assert (
        cli.main(["--config", str(config), "--state-file", str(tmp_path / "s.json")])
        == 2
    )
    assert "error" in capsys.readouterr().err
