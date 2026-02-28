from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
from typing import Any


class InMemoryBus:
    def __init__(self) -> None:
        self._topics: dict[str, list[dict[str, Any]]] = defaultdict(list)

    def publish(self, topic: str, message: dict[str, Any]) -> None:
        self._topics[topic].append(deepcopy(message))

    def consume(self, topic: str) -> list[dict[str, Any]]:
        return [deepcopy(item) for item in self._topics.get(topic, [])]