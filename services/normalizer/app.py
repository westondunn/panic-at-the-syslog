from __future__ import annotations


class NormalizerService:
    def health(self) -> dict[str, str]:
        return {"status": "ok", "service": "normalizer"}