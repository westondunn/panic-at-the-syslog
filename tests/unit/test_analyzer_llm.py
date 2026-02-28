"""Tests for LLM-backed analyzer insight generation."""

from __future__ import annotations

import json

import pytest

from libs.adapters.llm import LlmResponse, LlmUnavailableError, NullLlmAdapter
from services.analyzer.app import AnalyzerService, FindingRealtime
from services.analyzer.prompt import AnalyzerOutputError


def _make_finding(**overrides: object) -> FindingRealtime:
    defaults = {
        "finding_id": "find-llm-001",
        "correlation_id": "corr-llm-001",
        "category": "brute-force-suspected",
        "confidence": 0.82,
        "details": {"source_ip": "192.0.2.10", "attempts": 14},
    }
    defaults.update(overrides)
    return FindingRealtime(**defaults)  # type: ignore[arg-type]


class _FakeLlm:
    """In-memory LLM adapter returning a canned response."""

    def __init__(self, text: str) -> None:
        self._text = text

    def complete(self, prompt: str) -> LlmResponse:
        return LlmResponse(text=self._text)


class _FailingLlm:
    """LLM adapter that always raises LlmUnavailableError."""

    def complete(self, prompt: str) -> LlmResponse:
        raise LlmUnavailableError("test: endpoint down")


# -- Happy-path LLM insights --------------------------------------------------


def test_llm_insight_generation() -> None:
    """Inject a mock LLM returning valid JSON and verify the insight fields."""
    llm_output = json.dumps({
        "summary": "Brute-force attack detected.",
        "risk_level": "high",
        "recommended_actions": ["Block the source IP"],
        "confidence": 0.9,
        "evidence": ["14 failed login attempts in 60s"],
    })
    service = AnalyzerService(llm=_FakeLlm(llm_output))
    insight = service.generate_insight(_make_finding())

    assert insight.schema_version == "1.0"
    assert insight.summary == "Brute-force attack detected."
    assert "Block the source IP" in insight.recommendation
    assert insight.confidence == 0.9
    assert insight.finding_id == "find-llm-001"
    assert insight.correlation_id == "corr-llm-001"
    assert "evidence" in insight.details


def test_confidence_and_evidence_from_llm() -> None:
    """Verify that confidence and evidence from LLM appear in the insight."""
    llm_output = json.dumps({
        "summary": "WAN link instability observed.",
        "risk_level": "medium",
        "recommended_actions": ["Check ISP link health"],
        "confidence": 0.65,
        "evidence": ["5 flaps in 10 minutes", "Latency spike > 200ms"],
    })
    service = AnalyzerService(llm=_FakeLlm(llm_output))
    finding = _make_finding(category="wan-instability", confidence=0.6, details={})
    insight = service.generate_insight(finding)

    assert insight.confidence == 0.65
    assert insight.details["evidence"] == ["5 flaps in 10 minutes", "Latency spike > 200ms"]


# -- Rejection of non-JSON / invalid outputs ----------------------------------


def test_llm_rejects_non_json() -> None:
    """LLM returning plain text should be rejected and fall back to rules."""
    service = AnalyzerService(llm=_FakeLlm("not json at all"))
    insight = service.generate_insight(_make_finding())

    # Should fall back to rule-based insight
    assert insight.schema_version == "1.0"
    assert "brute-force-suspected" in insight.summary


def test_llm_rejects_schema_invalid() -> None:
    """LLM returning JSON missing required fields should fall back to rules."""
    bad_output = json.dumps({"summary": "partial data"})
    service = AnalyzerService(llm=_FakeLlm(bad_output))
    insight = service.generate_insight(_make_finding())

    # Should fall back to rule-based insight
    assert insight.schema_version == "1.0"
    assert "brute-force-suspected" in insight.summary


# -- Fallback to rules --------------------------------------------------------


def test_llm_unavailable_falls_back_to_rules() -> None:
    """When LLM endpoint is down, analyzer falls back to rule-based logic."""
    service = AnalyzerService(llm=_FailingLlm())
    insight = service.generate_insight(_make_finding())

    assert insight.schema_version == "1.0"
    assert insight.priority == "high"
    assert "brute-force-suspected" in insight.summary


def test_null_llm_uses_rules() -> None:
    """NullLlmAdapter (empty response) should trigger schema rejection and fallback."""
    service = AnalyzerService(llm=NullLlmAdapter())
    insight = service.generate_insight(_make_finding())

    assert insight.schema_version == "1.0"
    assert insight.priority == "high"


def test_no_llm_uses_rules() -> None:
    """AnalyzerService() with no LLM should use rule-based logic (backward compat)."""
    service = AnalyzerService()
    insight = service.generate_insight(_make_finding())

    assert insight.schema_version == "1.0"
    assert insight.priority == "high"
    assert insight.finding_id == "find-llm-001"


# -- Output validation directly ------------------------------------------------


def test_validate_llm_output_rejects_non_json() -> None:
    from services.analyzer.prompt import validate_llm_output

    with pytest.raises(AnalyzerOutputError, match="not valid JSON"):
        validate_llm_output("this is not json")


def test_validate_llm_output_rejects_missing_required() -> None:
    from services.analyzer.prompt import validate_llm_output

    with pytest.raises(AnalyzerOutputError, match="schema validation failed"):
        validate_llm_output(json.dumps({"summary": "partial"}))


def test_validate_llm_output_accepts_valid() -> None:
    from services.analyzer.prompt import validate_llm_output

    valid = json.dumps({
        "summary": "test",
        "risk_level": "low",
        "recommended_actions": ["do something"],
        "confidence": 0.5,
    })
    result = validate_llm_output(valid)
    assert result["summary"] == "test"
