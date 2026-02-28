from __future__ import annotations

from typing import Any

from libs.adapters.bus.in_memory import InMemoryBus


class NatsBusStub:
    """NATS adapter stub for non-default Tier 2 profile testing."""

    def __init__(self) -> None:
        self._delegate = InMemoryBus()

    def publish(self, topic: str, message: dict[str, Any]) -> None:
        self._delegate.publish(topic, message)

    def consume(self, topic: str) -> list[dict[str, Any]]:
        return self._delegate.consume(topic)