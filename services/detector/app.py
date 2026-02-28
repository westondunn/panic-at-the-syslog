from __future__ import annotations


class DetectorService:
    def health(self) -> dict[str, str]:
        return {"status": "ok", "service": "detector"}