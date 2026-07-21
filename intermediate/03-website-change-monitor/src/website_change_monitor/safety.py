"""URL safety checks.

Only ``http``/``https`` are allowed. To reduce server-side request forgery
(SSRF) risk, literal loopback, private, link-local, and reserved IP targets are
rejected, as is ``localhost``. Hostnames are not DNS-resolved here (that is a
deeper topic); this is a pragmatic first line of defence, documented as such.
"""

from __future__ import annotations

import ipaddress
from urllib.parse import urlsplit

from .errors import UnsafeUrlError

_BLOCKED_HOSTNAMES = {"localhost"}


def validate_url(url: str, *, allow_private: bool = False) -> None:
    """Raise :class:`UnsafeUrlError` if the URL should not be fetched."""
    parts = urlsplit(url)
    if parts.scheme not in {"http", "https"}:
        raise UnsafeUrlError(f"unsupported URL scheme: {parts.scheme or '(none)'}")
    host = parts.hostname
    if not host:
        raise UnsafeUrlError("URL has no host")
    if allow_private:
        return
    if host in _BLOCKED_HOSTNAMES or host.endswith(".localhost"):
        raise UnsafeUrlError(f"refusing to fetch local host: {host}")
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        return  # not a literal IP; allowed (see module note)
    if (
        address.is_loopback
        or address.is_private
        or address.is_link_local
        or address.is_reserved
    ):
        raise UnsafeUrlError(f"refusing to fetch private/reserved address: {host}")
