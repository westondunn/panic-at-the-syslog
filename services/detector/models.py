from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Finding:
    finding_id: str
    correlation_id: str
    detected_at: str
    category: str
    confidence: float
    severity: str
    evidence: list[dict[str, Any]]
    details: dict[str, Any]

    def to_event(self) -> dict[str, Any]:
        return {
            "schema_version": "1.0",
            "finding_id": self.finding_id,
            "correlation_id": self.correlation_id,
            "detected_at": self.detected_at,
            "category": self.category,
            "confidence": self.confidence,
            "severity": self.severity,
            "evidence": self.evidence,
            "details": self.details,
        }
