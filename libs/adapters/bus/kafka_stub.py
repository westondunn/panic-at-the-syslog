from __future__ import annotations

from typing import Any

from libs.adapters.bus.in_memory import InMemoryBus


class KafkaBusStub:
    """Kafka adapter stub for Tier 1 scaffolding.

    This placeholder intentionally avoids external broker dependencies.
    """

    def __init__(self) -> None:
        self._delegate = InMemoryBus()

    def publish(self, topic: str, message: dict[str, Any]) -> None:
        self._delegate.publish(topic, message)

    def consume(self, topic: str) -> list[dict[str, Any]]:
        return self._delegate.consume(topic)