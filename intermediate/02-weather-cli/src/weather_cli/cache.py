"""A small time-to-live file cache for successful provider responses.

Caching briefly is friendlier to the free provider and speeds up repeated runs.
The clock is injectable so cache expiry can be tested deterministically.
"""

from __future__ import annotations

import hashlib
import json
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

Clock = Callable[[], float]


class FileCache:
    def __init__(
        self,
        directory: Path,
        ttl_seconds: float,
        now: Clock = time.time,
    ) -> None:
        self._directory = directory
        self._ttl = ttl_seconds
        self._now = now

    def _path_for(self, key: str) -> Path:
        digest = hashlib.sha256(key.encode("utf-8")).hexdigest()[:32]
        return self._directory / f"{digest}.json"

    def get(self, key: str) -> Any | None:
        path = self._path_for(key)
        if not path.is_file():
            return None
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
            stored_at = float(record["stored_at"])
            payload = record["payload"]
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            return None
        if self._now() - stored_at > self._ttl:
            return None
        return payload

    def set(self, key: str, payload: Any) -> None:
        self._directory.mkdir(parents=True, exist_ok=True)
        record = {"stored_at": self._now(), "payload": payload}
        self._path_for(key).write_text(
            json.dumps(record), encoding="utf-8", newline="\n"
        )
