from __future__ import annotations

from typing import Any, Protocol


class MessageBus(Protocol):
    def publish(self, topic: str, message: dict[str, Any]) -> None: ...

    def consume(self, topic: str) -> list[dict[str, Any]]: ...