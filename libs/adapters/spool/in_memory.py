from __future__ import annotations

import time
from copy import deepcopy
from typing import Any

from libs.common.logging import get_logger

logger = get_logger(__name__)


class InMemorySpool:
    """In-memory spool for testing and lightweight workloads."""

    def __init__(self) -> None:
        self._entries: list[tuple[float, dict[str, Any]]] = []

    def write(self, message: dict[str, Any]) -> None:
        ts = time.time()
        self._entries.append((ts, deepcopy(message)))
        logger.debug("spooled message at ts=%s", ts)

    def read_all(self) -> list[dict[str, Any]]:
        return [deepcopy(msg) for _, msg in self._entries]

    def purge_expired(self, ttl_seconds: int) -> int:
        cutoff = time.time() - ttl_seconds
        before = len(self._entries)
        self._entries = [(ts, msg) for ts, msg in self._entries if ts > cutoff]
        purged = before - len(self._entries)
        if purged:
            logger.info("purged %d expired entries (ttl=%ds)", purged, ttl_seconds)
        return purged
