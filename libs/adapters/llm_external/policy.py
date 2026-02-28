from __future__ import annotations

import re
import time
from dataclasses import dataclass, field
from typing import Any


# ---------------------------------------------------------------------------
# Redaction
# ---------------------------------------------------------------------------

_IP_RE = re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b")
_MAC_RE = re.compile(r"\b(?:[0-9a-fA-F]{2}[:\-]){5}[0-9a-fA-F]{2}\b")
_HOSTNAME_RE = re.compile(
    r"\b(?!(?:\d{1,3}\.){3}\d{1,3}\b)[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?"
    r"(?:\.[a-zA-Z]{2,})+\b"
)


def redact_prompt(text: str) -> str:
    """Replace IPs, MACs, and FQDNs with stable placeholder tokens."""
    text = _IP_RE.sub("<REDACTED_IP>", text)
    text = _MAC_RE.sub("<REDACTED_MAC>", text)
    text = _HOSTNAME_RE.sub("<REDACTED_HOST>", text)
    return text


# ---------------------------------------------------------------------------
# Audit
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class AuditEntry:
    timestamp: float
    correlation_id: str
    prompt_version: str
    redaction_enabled: bool
    response_hash: str
    model_id: str
    token_usage: int | None = None
    reason: str = ""


class AuditLog:
    """Append-only in-memory audit log for external LLM calls."""

    def __init__(self) -> None:
        self._entries: list[AuditEntry] = []

    def record(self, entry: AuditEntry) -> None:
        self._entries.append(entry)

    @property
    def entries(self) -> list[AuditEntry]:
        return list(self._entries)


# ---------------------------------------------------------------------------
# Budget
# ---------------------------------------------------------------------------

@dataclass
class BudgetPolicy:
    """Token/cost budget enforced per calendar day and month."""

    daily_token_limit: int = 100_000
    monthly_token_limit: int = 2_000_000
    _daily_used: int = field(default=0, repr=False)
    _monthly_used: int = field(default=0, repr=False)

    def record_usage(self, tokens: int) -> None:
        self._daily_used += tokens
        self._monthly_used += tokens

    def check(self, estimated_tokens: int = 0) -> bool:
        """Return ``True`` if the request is within budget."""
        return (
            self._daily_used + estimated_tokens <= self.daily_token_limit
            and self._monthly_used + estimated_tokens <= self.monthly_token_limit
        )

    def reset_daily(self) -> None:
        self._daily_used = 0

    def reset_monthly(self) -> None:
        self._monthly_used = 0
        self._daily_used = 0


# ---------------------------------------------------------------------------
# Circuit breaker
# ---------------------------------------------------------------------------

@dataclass
class CircuitBreaker:
    """Simple consecutive-failure circuit breaker."""

    failure_threshold: int = 5
    recovery_timeout: float = 60.0
    _consecutive_failures: int = field(default=0, repr=False)
    _opened_at: float | None = field(default=None, repr=False)

    @property
    def is_open(self) -> bool:
        if self._opened_at is None:
            return False
        if time.monotonic() - self._opened_at >= self.recovery_timeout:
            # half-open: allow one probe
            return False
        return True

    def record_success(self) -> None:
        self._consecutive_failures = 0
        self._opened_at = None

    def record_failure(self) -> None:
        self._consecutive_failures += 1
        if self._consecutive_failures >= self.failure_threshold:
            self._opened_at = time.monotonic()

    def reset(self) -> None:
        self._consecutive_failures = 0
        self._opened_at = None


# ---------------------------------------------------------------------------
# Composite policy gate
# ---------------------------------------------------------------------------

@dataclass
class PolicyGate:
    """Aggregates all governance checks into a single gate."""

    redaction_enabled: bool = True
    budget: BudgetPolicy = field(default_factory=BudgetPolicy)
    circuit_breaker: CircuitBreaker = field(default_factory=CircuitBreaker)
    audit_log: AuditLog = field(default_factory=AuditLog)

    def pre_request(self, prompt: str, *, estimated_tokens: int = 0) -> dict[str, Any]:
        """Run policy checks *before* an external call.

        Returns a dict with ``allowed`` (bool) and the potentially redacted
        ``prompt``.  When disallowed, includes a ``reason``.
        """
        if self.circuit_breaker.is_open:
            return {"allowed": False, "prompt": prompt, "reason": "circuit_breaker_open"}

        if not self.budget.check(estimated_tokens):
            return {"allowed": False, "prompt": prompt, "reason": "budget_exceeded"}

        if self.redaction_enabled:
            prompt = redact_prompt(prompt)

        return {"allowed": True, "prompt": prompt}

    def post_request(
        self,
        *,
        correlation_id: str,
        prompt_version: str,
        response_hash: str,
        model_id: str,
        token_usage: int | None = None,
        success: bool = True,
        reason: str = "",
    ) -> None:
        """Record outcome and update policy state after an external call."""
        if success:
            self.circuit_breaker.record_success()
        else:
            self.circuit_breaker.record_failure()

        if token_usage is not None:
            self.budget.record_usage(token_usage)

        self.audit_log.record(
            AuditEntry(
                timestamp=time.time(),
                correlation_id=correlation_id,
                prompt_version=prompt_version,
                redaction_enabled=self.redaction_enabled,
                response_hash=response_hash,
                model_id=model_id,
                token_usage=token_usage,
                reason=reason,
            )
        )
