"""External LLM provider plugin boundary.

This module is **disabled by default** and must be explicitly enabled by an
administrator.  All external calls are governed by policy hooks: redaction,
audit logging, budgets, and a circuit breaker.

See ``docs/governance/ai-fallback.md`` for operational guidance.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import Any, Callable

from libs.adapters.llm import LlmAdapter, LlmResponse

logger = logging.getLogger(__name__)


@dataclass
class LlmPolicy:
    """Governance policy for external LLM calls."""

    redaction_enabled: bool = True
    audit_callback: Callable[[dict[str, Any]], None] | None = None
    budget_remaining: float = 1000.0
    circuit_breaker_threshold: int = 5


class CircuitOpenError(Exception):
    """Raised when the circuit breaker has tripped."""


class BudgetExhaustedError(Exception):
    """Raised when the token/cost budget is exhausted."""


class ExternalLlmPlugin:
    """Governed external LLM provider plugin.

    Implements ``LlmAdapter`` but enforces policy hooks before every call.
    **Disabled by default** — instantiate with ``enabled=True`` to activate.
    """

    def __init__(
        self,
        enabled: bool = False,
        policy: LlmPolicy | None = None,
        delegate: LlmAdapter | None = None,
    ) -> None:
        self.enabled = enabled
        self.policy = policy or LlmPolicy()
        self._delegate = delegate
        self._consecutive_failures: int = 0

    # -- LlmAdapter protocol --------------------------------------------------

    def complete(self, prompt: str) -> LlmResponse:
        if not self.enabled:
            raise RuntimeError("External LLM plugin is disabled by default")

        self._check_circuit_breaker()
        self._check_budget()

        safe_prompt = self._redact(prompt) if self.policy.redaction_enabled else prompt

        try:
            response = self._call_delegate(safe_prompt)
        except Exception:
            self._consecutive_failures += 1
            raise

        self._consecutive_failures = 0
        self._audit(prompt=safe_prompt, response=response)
        return response

    # -- Policy hooks ----------------------------------------------------------

    def _check_circuit_breaker(self) -> None:
        if self._consecutive_failures >= self.policy.circuit_breaker_threshold:
            raise CircuitOpenError(
                f"Circuit breaker open after {self._consecutive_failures} consecutive failures"
            )

    def _check_budget(self) -> None:
        if self.policy.budget_remaining <= 0:
            raise BudgetExhaustedError("External LLM budget exhausted")

    def _redact(self, text: str) -> str:
        """Replace potentially sensitive tokens with placeholders.

        This is a baseline implementation — production deployments should
        extend with regex-based or NER-based redaction.
        """
        # Redact IPv4 addresses
        text = re.sub(
            r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
            "[REDACTED_IP]",
            text,
        )
        # Redact MAC addresses
        text = re.sub(
            r"\b(?:[0-9a-fA-F]{2}[:\-]){5}[0-9a-fA-F]{2}\b",
            "[REDACTED_MAC]",
            text,
        )
        return text

    def _audit(self, *, prompt: str, response: LlmResponse) -> None:
        record: dict[str, Any] = {
            "action": "external_llm_call",
            "model": response.model,
            "redaction_enabled": self.policy.redaction_enabled,
            "response_length": len(response.text),
        }
        if self.policy.audit_callback is not None:
            self.policy.audit_callback(record)
        else:
            logger.info("external llm audit: %s", record)

    def _call_delegate(self, prompt: str) -> LlmResponse:
        if self._delegate is None:
            raise RuntimeError("No delegate LLM adapter configured for external plugin")
        return self._delegate.complete(prompt)
