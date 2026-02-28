from __future__ import annotations

import time

import pytest

from libs.adapters.llm import LlmResponse
from libs.adapters.llm_external.policy import (
    AuditLog,
    BudgetPolicy,
    CircuitBreaker,
    PolicyGate,
    redact_prompt,
)
from libs.adapters.llm_external.provider import ExternalLlmProvider


# ---------------------------------------------------------------------------
# Redaction
# ---------------------------------------------------------------------------


def test_redact_prompt_masks_ips() -> None:
    assert "<REDACTED_IP>" in redact_prompt("source 192.168.1.1 destination 10.0.0.5")


def test_redact_prompt_masks_macs() -> None:
    assert "<REDACTED_MAC>" in redact_prompt("device aa:bb:cc:dd:ee:ff seen")


def test_redact_prompt_masks_hostnames() -> None:
    assert "<REDACTED_HOST>" in redact_prompt("resolved host.example.com to addr")


def test_redact_prompt_preserves_plain_text() -> None:
    text = "no sensitive tokens here"
    assert redact_prompt(text) == text


# ---------------------------------------------------------------------------
# Audit log
# ---------------------------------------------------------------------------


def test_audit_log_records_and_returns_entries() -> None:
    from libs.adapters.llm_external.policy import AuditEntry

    log = AuditLog()
    entry = AuditEntry(
        timestamp=time.time(),
        correlation_id="corr-1",
        prompt_version="1.0",
        redaction_enabled=True,
        response_hash="abc123",
        model_id="gpt-test",
    )
    log.record(entry)
    assert len(log.entries) == 1
    assert log.entries[0].correlation_id == "corr-1"


# ---------------------------------------------------------------------------
# Budget
# ---------------------------------------------------------------------------


def test_budget_allows_within_limits() -> None:
    budget = BudgetPolicy(daily_token_limit=1000, monthly_token_limit=5000)
    assert budget.check(estimated_tokens=500) is True


def test_budget_rejects_when_daily_exceeded() -> None:
    budget = BudgetPolicy(daily_token_limit=100, monthly_token_limit=5000)
    budget.record_usage(100)
    assert budget.check(estimated_tokens=1) is False


def test_budget_rejects_when_monthly_exceeded() -> None:
    budget = BudgetPolicy(daily_token_limit=100_000, monthly_token_limit=200)
    budget.record_usage(200)
    assert budget.check(estimated_tokens=1) is False


def test_budget_reset_daily() -> None:
    budget = BudgetPolicy(daily_token_limit=100, monthly_token_limit=5000)
    budget.record_usage(100)
    assert budget.check(estimated_tokens=1) is False
    budget.reset_daily()
    assert budget.check(estimated_tokens=1) is True


# ---------------------------------------------------------------------------
# Circuit breaker
# ---------------------------------------------------------------------------


def test_circuit_breaker_closed_by_default() -> None:
    cb = CircuitBreaker(failure_threshold=3)
    assert cb.is_open is False


def test_circuit_breaker_opens_on_threshold() -> None:
    cb = CircuitBreaker(failure_threshold=3, recovery_timeout=60.0)
    cb.record_failure()
    cb.record_failure()
    assert cb.is_open is False
    cb.record_failure()
    assert cb.is_open is True


def test_circuit_breaker_resets_on_success() -> None:
    cb = CircuitBreaker(failure_threshold=2)
    cb.record_failure()
    cb.record_success()
    cb.record_failure()
    assert cb.is_open is False


# ---------------------------------------------------------------------------
# PolicyGate
# ---------------------------------------------------------------------------


def test_policy_gate_allows_normal_request() -> None:
    gate = PolicyGate()
    result = gate.pre_request("check host 10.0.0.1")
    assert result["allowed"] is True
    assert "<REDACTED_IP>" in result["prompt"]


def test_policy_gate_blocks_when_breaker_open() -> None:
    cb = CircuitBreaker(failure_threshold=1)
    cb.record_failure()
    gate = PolicyGate(circuit_breaker=cb)
    result = gate.pre_request("anything")
    assert result["allowed"] is False
    assert result["reason"] == "circuit_breaker_open"


def test_policy_gate_blocks_when_budget_exceeded() -> None:
    budget = BudgetPolicy(daily_token_limit=0, monthly_token_limit=0)
    gate = PolicyGate(budget=budget)
    result = gate.pre_request("anything", estimated_tokens=1)
    assert result["allowed"] is False
    assert result["reason"] == "budget_exceeded"


def test_policy_gate_redaction_can_be_disabled() -> None:
    gate = PolicyGate(redaction_enabled=False)
    prompt = "ip 10.0.0.1"
    result = gate.pre_request(prompt)
    assert result["prompt"] == prompt


# ---------------------------------------------------------------------------
# ExternalLlmProvider
# ---------------------------------------------------------------------------


def test_provider_disabled_by_default() -> None:
    provider = ExternalLlmProvider()
    with pytest.raises(RuntimeError, match="disabled"):
        provider.complete("hello")


def test_provider_stub_mode_returns_response() -> None:
    provider = ExternalLlmProvider(enabled=True)
    resp = provider.complete("test prompt", correlation_id="corr-1")
    assert resp.text.startswith("external-stub-response:")


def test_provider_records_audit_entry() -> None:
    provider = ExternalLlmProvider(enabled=True)
    provider.complete("audit me", correlation_id="corr-2")
    entries = provider.policy.audit_log.entries
    assert len(entries) == 1
    assert entries[0].correlation_id == "corr-2"
    assert entries[0].response_hash != ""


def test_provider_respects_budget_policy() -> None:
    budget = BudgetPolicy(daily_token_limit=0, monthly_token_limit=0)
    policy = PolicyGate(budget=budget)
    provider = ExternalLlmProvider(enabled=True, policy=policy)
    with pytest.raises(RuntimeError, match="budget_exceeded"):
        provider.complete("anything", correlation_id="corr-3")


def test_provider_respects_circuit_breaker() -> None:
    cb = CircuitBreaker(failure_threshold=1)
    cb.record_failure()
    policy = PolicyGate(circuit_breaker=cb)
    provider = ExternalLlmProvider(enabled=True, policy=policy)
    with pytest.raises(RuntimeError, match="circuit_breaker_open"):
        provider.complete("anything", correlation_id="corr-4")


def test_provider_delegates_to_inner_adapter() -> None:
    class FakeInner:
        def complete(self, prompt: str) -> LlmResponse:
            return LlmResponse(text=f"inner:{prompt[:20]}")

    provider = ExternalLlmProvider(enabled=True, inner=FakeInner())
    resp = provider.complete("delegate test", correlation_id="corr-5")
    assert resp.text.startswith("inner:")


def test_provider_redacts_before_inner_call() -> None:
    captured: list[str] = []

    class CapturingInner:
        def complete(self, prompt: str) -> LlmResponse:
            captured.append(prompt)
            return LlmResponse(text="ok")

    provider = ExternalLlmProvider(enabled=True, inner=CapturingInner())
    provider.complete("check 192.168.1.1", correlation_id="corr-6")
    assert "<REDACTED_IP>" in captured[0]
    assert "192.168.1.1" not in captured[0]
