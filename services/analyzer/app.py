from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import UTC, datetime
from hashlib import sha256
from typing import Any

from libs.adapters.llm import LlmAdapter, LlmUnavailableError
from services.analyzer.prompt import (
    AnalyzerOutputError,
    render_prompt,
    validate_llm_output,
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class FindingRealtime:
    finding_id: str
    correlation_id: str
    category: str
    confidence: float
    details: dict[str, Any]


@dataclass(frozen=True)
class InsightRecommendation:
    schema_version: str
    insight_id: str
    finding_id: str
    correlation_id: str
    analyzed_at: str
    summary: str
    recommendation: str
    rationale: str
    priority: str
    confidence: float
    details: dict[str, Any]

    def to_event(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "insight_id": self.insight_id,
            "finding_id": self.finding_id,
            "correlation_id": self.correlation_id,
            "analyzed_at": self.analyzed_at,
            "summary": self.summary,
            "recommendation": self.recommendation,
            "rationale": self.rationale,
            "priority": self.priority,
            "confidence": self.confidence,
            "details": self.details,
        }


class AnalyzerService:
    def __init__(self, llm: LlmAdapter | None = None) -> None:
        self._llm = llm

    def health(self) -> dict[str, str]:
        return {"status": "ok", "service": "analyzer"}

    def generate_insight(self, finding: FindingRealtime) -> InsightRecommendation:
        if self._llm is not None:
            try:
                return self._generate_insight_llm(finding)
            except (LlmUnavailableError, AnalyzerOutputError) as exc:
                logger.warning("LLM analysis failed, falling back to rules: %s", exc)

        return self._generate_insight_rules(finding)

    # -- LLM-backed path ------------------------------------------------------

    def _generate_insight_llm(self, finding: FindingRealtime) -> InsightRecommendation:
        prompt = render_prompt(
            category=finding.category,
            confidence=finding.confidence,
            details=finding.details,
        )
        response = self._llm.complete(prompt)  # type: ignore[union-attr]
        parsed = validate_llm_output(response.text)

        normalized_confidence = min(max(parsed.get("confidence", finding.confidence), 0.0), 1.0)
        insight_id = self._build_insight_id(finding.finding_id)
        priority = self._derive_priority(normalized_confidence)
        evidence = parsed.get("evidence", [])

        return InsightRecommendation(
            schema_version="1.0",
            insight_id=insight_id,
            finding_id=finding.finding_id,
            correlation_id=finding.correlation_id,
            analyzed_at=datetime.now(UTC).isoformat().replace("+00:00", "Z"),
            summary=parsed["summary"],
            recommendation="; ".join(parsed["recommended_actions"]),
            rationale=parsed.get(
                "notes",
                f"LLM analysis for category '{finding.category}' "
                f"with confidence {normalized_confidence:.2f}.",
            ),
            priority=priority,
            confidence=normalized_confidence,
            details={**finding.details, "category": finding.category, "evidence": evidence},
        )

    # -- Rule-based fallback path ----------------------------------------------

    def _generate_insight_rules(self, finding: FindingRealtime) -> InsightRecommendation:
        normalized_confidence = min(max(finding.confidence, 0.0), 1.0)
        insight_id = self._build_insight_id(finding.finding_id)
        priority = self._derive_priority(normalized_confidence)

        summary = (
            f"Finding category '{finding.category}' requires follow-up review and remediation."
        )
        recommendation = self._derive_recommendation(finding.category)

        attempt_count = finding.details.get("attempts")
        rationale = (
            f"Confidence score is {normalized_confidence:.2f}; "
            f"detector category is '{finding.category}'."
        )
        if attempt_count is not None:
            rationale = (
                f"{rationale} Observed {attempt_count} related attempts in detector context."
            )

        return InsightRecommendation(
            schema_version="1.0",
            insight_id=insight_id,
            finding_id=finding.finding_id,
            correlation_id=finding.correlation_id,
            analyzed_at=datetime.now(UTC).isoformat().replace("+00:00", "Z"),
            summary=summary,
            recommendation=recommendation,
            rationale=rationale,
            priority=priority,
            confidence=normalized_confidence,
            details={**finding.details, "category": finding.category},
        )

    def _build_insight_id(self, finding_id: str) -> str:
        digest = sha256(f"1.0:{finding_id}".encode("utf-8")).hexdigest()[:16]
        return f"ins-{digest}"

    def _derive_priority(self, confidence: float) -> str:
        if confidence >= 0.9:
            return "critical"
        if confidence >= 0.75:
            return "high"
        if confidence >= 0.5:
            return "medium"
        return "low"

    def _derive_recommendation(self, category: str) -> str:
        if category == "brute-force-suspected":
            return "Block the source IP at the edge and require MFA for targeted accounts."
        if category == "wan-instability":
            return "Inspect WAN link health and failover policy, then validate ISP path stability."
        if category == "dns-anomaly":
            return "Review resolver policy and block suspicious domains at DNS egress controls."
        return "Review evidence, validate impact scope, and apply least-disruptive containment."
