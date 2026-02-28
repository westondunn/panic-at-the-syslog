from __future__ import annotations

from typing import Any, Protocol


class SpoolWriter(Protocol):
    """Accepts messages for temporary spooling."""

    def write(self, message: dict[str, Any]) -> None: ...


class SpoolReader(Protocol):
    """Reads and manages spooled messages."""

    def read_all(self) -> list[dict[str, Any]]: ...

    def purge_expired(self, ttl_seconds: int) -> int: ...
