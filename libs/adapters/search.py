from __future__ import annotations

from typing import Any, Protocol


class SearchAdapter(Protocol):
    def index(self, index_name: str, document: dict[str, Any]) -> None: ...

    def query(self, index_name: str, term: str) -> list[dict[str, Any]]: ...


class InMemorySearch:
    def __init__(self) -> None:
        self._indexes: dict[str, list[dict[str, Any]]] = {}

    def index(self, index_name: str, document: dict[str, Any]) -> None:
        self._indexes.setdefault(index_name, []).append(dict(document))

    def query(self, index_name: str, term: str) -> list[dict[str, Any]]:
        documents = self._indexes.get(index_name, [])
        return [doc for doc in documents if term.lower() in str(doc).lower()]