"""Bounded, timed HTTP fetching.

Fetches send a clear user agent, use connect/read timeouts, cap redirects, and
stop reading once a maximum byte budget is exceeded. Only ``text/*`` responses
are accepted.
"""

from __future__ import annotations

import httpx

from .errors import FetchError

USER_AGENT = (
    "website-change-monitor/0.1 "
    "(+https://github.com/vietIT2002/practical-python-projects)"
)
DEFAULT_TIMEOUT = httpx.Timeout(connect=5.0, read=10.0, write=10.0, pool=5.0)
DEFAULT_MAX_REDIRECTS = 5
DEFAULT_MAX_BYTES = 2_000_000


def create_http_client(
    timeout: httpx.Timeout = DEFAULT_TIMEOUT,
    max_redirects: int = DEFAULT_MAX_REDIRECTS,
) -> httpx.Client:
    return httpx.Client(
        timeout=timeout,
        follow_redirects=True,
        max_redirects=max_redirects,
        headers={"User-Agent": USER_AGENT},
    )


def fetch(client: httpx.Client, url: str, *, max_bytes: int = DEFAULT_MAX_BYTES) -> str:
    """Fetch ``url`` and return its text, enforcing size and type limits."""
    try:
        with client.stream("GET", url) as response:
            if response.status_code >= 400:
                raise FetchError(f"HTTP {response.status_code}")
            content_type = response.headers.get("content-type", "")
            if not content_type.startswith("text/"):
                raise FetchError(
                    f"unsupported content type: {content_type or '(none)'}"
                )
            body = bytearray()
            for chunk in response.iter_bytes():
                body += chunk
                if len(body) > max_bytes:
                    raise FetchError(f"response exceeded {max_bytes} bytes")
            return body.decode(response.encoding or "utf-8", errors="replace")
    except httpx.TooManyRedirects as exc:
        raise FetchError("too many redirects") from exc
    except httpx.TimeoutException as exc:
        raise FetchError("timed out") from exc
    except httpx.TransportError as exc:
        raise FetchError(f"could not connect: {exc}") from exc
