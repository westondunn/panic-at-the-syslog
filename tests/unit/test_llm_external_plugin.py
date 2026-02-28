"""Tests for the external LLM provider plugin (Issue #28)."""

from __future__ import annotations

import pytest

from libs.adapters.llm import LlmResponse
from libs.adapters.llm_external_plugin import (
    BudgetExhaustedError,
    CircuitOpenError,
    ExternalLlmPlugin,
    LlmPolicy,
)


class _FakeDelegate:
    """Minimal LLM adapter for testing the plugin wrapper."""

    def __init__(self, text: str = '{"result": "ok"}') -> None:
        self._text = text
        self.last_prompt: str | None = None

    def complete(self, prompt: str) -> LlmResponse:
        self.last_prompt = prompt
        return LlmResponse(text=self._text, model="test-model")


class _FailingDelegate:
    """LLM adapter that always raises."""

    def complete(self, prompt: str) -> LlmResponse:
        raise ConnectionError("boom")


def test_external_plugin_disabled_by_default() -> None:
    """Plugin raises when not explicitly enabled."""
    plugin = ExternalLlmPlugin()
    with pytest.raises(RuntimeError, match="disabled by default"):
        plugin.complete("test prompt")


def test_external_plugin_enabled_happy_path() -> None:
    """Enabled plugin delegates to the underlying adapter."""
    delegate = _FakeDelegate("hello")
    plugin = ExternalLlmPlugin(enabled=True, delegate=delegate)
    resp = plugin.complete("test")
    assert resp.text == "hello"


def test_external_plugin_policy_redaction() -> None:
    """Sensitive data (IPs, MACs) should be redacted before the delegate call."""
    delegate = _FakeDelegate()
    policy = LlmPolicy(redaction_enabled=True)
    plugin = ExternalLlmPlugin(enabled=True, policy=policy, delegate=delegate)

    plugin.complete("failed login from 192.168.1.100 mac aa:bb:cc:dd:ee:ff")
    assert delegate.last_prompt is not None
    assert "192.168.1.100" not in delegate.last_prompt
    assert "[REDACTED_IP]" in delegate.last_prompt
    assert "aa:bb:cc:dd:ee:ff" not in delegate.last_prompt
    assert "[REDACTED_MAC]" in delegate.last_prompt


def test_external_plugin_budget_exhausted() -> None:
    """Plugin refuses calls when budget is zero."""
    policy = LlmPolicy(budget_remaining=0)
    plugin = ExternalLlmPlugin(enabled=True, policy=policy, delegate=_FakeDelegate())

    with pytest.raises(BudgetExhaustedError, match="budget exhausted"):
        plugin.complete("test")


def test_external_plugin_circuit_breaker_trips() -> None:
    """After N consecutive failures the circuit breaker opens."""
    policy = LlmPolicy(circuit_breaker_threshold=3)
    plugin = ExternalLlmPlugin(enabled=True, policy=policy, delegate=_FailingDelegate())

    for _ in range(3):
        with pytest.raises(ConnectionError):
            plugin.complete("test")

    # Now the breaker should be open
    with pytest.raises(CircuitOpenError, match="Circuit breaker open"):
        plugin.complete("test")


def test_external_plugin_circuit_breaker_resets_on_success() -> None:
    """A successful call resets the consecutive failure counter."""
    delegate = _FakeDelegate()
    policy = LlmPolicy(circuit_breaker_threshold=3)
    plugin = ExternalLlmPlugin(enabled=True, policy=policy, delegate=delegate)

    # Simulate 2 failures (below threshold)
    plugin._consecutive_failures = 2
    resp = plugin.complete("test")
    assert resp.text == '{"result": "ok"}'
    assert plugin._consecutive_failures == 0


def test_external_plugin_audit_callback() -> None:
    """Audit callback is invoked with expected record shape."""
    audit_records: list[dict] = []

    def audit_cb(record: dict) -> None:
        audit_records.append(record)

    policy = LlmPolicy(audit_callback=audit_cb)
    delegate = _FakeDelegate("response text")
    plugin = ExternalLlmPlugin(enabled=True, policy=policy, delegate=delegate)

    plugin.complete("some prompt")

    assert len(audit_records) == 1
    record = audit_records[0]
    assert record["action"] == "external_llm_call"
    assert record["model"] == "test-model"
    assert record["redaction_enabled"] is True
