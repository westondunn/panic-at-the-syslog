from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from typing import Any

from libs.common.logging import get_logger

logger = get_logger(__name__)


class DiskSpool:
    """Disk-based spool that persists each message as a separate JSON file.

    Filename format: ``{timestamp}_{event_id}.json``
    """

    def __init__(self, directory: str | Path) -> None:
        self._directory = Path(directory)
        self._directory.mkdir(parents=True, exist_ok=True)

    def write(self, message: dict[str, Any]) -> None:
        ts = time.time()
        event_id = uuid.uuid4().hex
        filename = f"{ts}_{event_id}.json"
        path = self._directory / filename
        path.write_text(json.dumps(message), encoding="utf-8")
        logger.debug("wrote spool file %s", filename)

    def read_all(self) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        for path in sorted(self._directory.glob("*.json")):
            try:
                results.append(json.loads(path.read_text(encoding="utf-8")))
            except (json.JSONDecodeError, OSError):
                logger.warning("skipping unreadable spool file %s", path.name)
        return results

    def purge_expired(self, ttl_seconds: int) -> int:
        cutoff = time.time() - ttl_seconds
        purged = 0
        for path in self._directory.glob("*.json"):
            try:
                file_ts = float(path.name.split("_", 1)[0])
            except (ValueError, IndexError):
                logger.warning("skipping file with unparseable name %s", path.name)
                continue
            if file_ts <= cutoff:
                path.unlink()
                purged += 1
        if purged:
            logger.info("purged %d expired files (ttl=%ds)", purged, ttl_seconds)
        return purged
