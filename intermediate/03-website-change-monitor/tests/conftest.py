"""Shared test helpers: build httpx clients backed by a mock transport."""

from __future__ import annotations

from collections.abc import Callable

import httpx
import pytest

Handler = Callable[[httpx.Request], httpx.Response]


@pytest.fixture
def client_from() -> Callable[..., httpx.Client]:
    def make(handler: Handler, **client_kwargs: object) -> httpx.Client:
        return httpx.Client(transport=httpx.MockTransport(handler), **client_kwargs)  # type: ignore[arg-type]

    return make


@pytest.fixture
def html_client(
    client_from: Callable[..., httpx.Client],
) -> Callable[..., httpx.Client]:
    def make(
        body: str = "<html>hello</html>",
        content_type: str = "text/html; charset=utf-8",
        status: int = 200,
    ) -> httpx.Client:
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(
                status, headers={"content-type": content_type}, content=body.encode()
            )

        return client_from(handler)

    return make
