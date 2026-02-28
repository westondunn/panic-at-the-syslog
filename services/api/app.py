from __future__ import annotations


class ApiService:
    def health(self) -> dict[str, str]:
        return {"status": "ok", "service": "api"}