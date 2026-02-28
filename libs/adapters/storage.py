from __future__ import annotations

from typing import Any, Protocol


class StorageAdapter(Protocol):
    def upsert(self, collection: str, item_id: str, data: dict[str, Any]) -> None: ...

    def get(self, collection: str, item_id: str) -> dict[str, Any] | None: ...


class InMemoryStorage:
    def __init__(self) -> None:
        self._data: dict[str, dict[str, dict[str, Any]]] = {}

    def upsert(self, collection: str, item_id: str, data: dict[str, Any]) -> None:
        self._data.setdefault(collection, {})[item_id] = dict(data)

    def get(self, collection: str, item_id: str) -> dict[str, Any] | None:
        item = self._data.get(collection, {}).get(item_id)
        return dict(item) if item is not None else None