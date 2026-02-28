from __future__ import annotations


class AnalyzerService:
    def health(self) -> dict[str, str]:
        return {"status": "ok", "service": "analyzer"}