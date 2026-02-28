from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Any

from libs.adapters.bus.interface import MessageBus
from libs.common.logging import get_logger

from .rules import (
    detect_brute_force,
    detect_dhcp_churn,
    detect_firewall_denies,
    detect_wan_flaps,
)

_RULES = [
    detect_brute_force,
    detect_wan_flaps,
    detect_firewall_denies,
    detect_dhcp_churn,
]

_DLQ_TOPIC = "dlq.detector.v1"
_SOURCE_TOPIC = "events.normalized.v1"


def _build_dlq_id(error: str, event_ids: list[str]) -> str:
    blob = f"dlq:detector:{error}:{'|'.join(sorted(event_ids))}"
    return hashlib.sha256(blob.encode()).hexdigest()


class DetectorService:
    def __init__(self, bus: MessageBus | None = None) -> None:
        self.bus = bus
        self.logger = get_logger("panic.services.detector")

    def health(self) -> dict[str, str]:
        return {"status": "ok", "service": "detector"}

    def process(self, events: list[dict[str, Any]]) -> list[dict[str, Any]]:
        all_findings: list[dict[str, Any]] = []
        for rule in _RULES:
            try:
                findings = rule(events)
            except Exception as exc:
                self._send_to_dlq(events, rule.__name__, exc)
                continue
            for finding in findings:
                finding_event = finding.to_event()
                all_findings.append(finding_event)
                self.logger.info(
                    "finding detected: %s",
                    finding.category,
                    extra={
                        "correlation_id": finding.correlation_id,
                        "finding_id": finding.finding_id,
                    },
                )
                if self.bus is not None:
                    self.bus.publish("findings.realtime.v1", finding_event)
        return all_findings

    def _send_to_dlq(
        self,
        events: list[dict[str, Any]],
        rule_name: str,
        exc: Exception,
    ) -> None:
        correlation_id = events[0].get("correlation_id", "") if events else ""
        event_ids = [e.get("event_id", "") for e in events]
        error_msg = f"error in rule {rule_name}: {exc}"
        error_type = "validation" if "ValidationError" in type(exc).__name__ else "rule_error"
        dlq_event: dict[str, Any] = {
            "schema_version": "1.0",
            "dlq_id": _build_dlq_id(error_msg, event_ids),
            "correlation_id": correlation_id,
            "failed_at": datetime.now(timezone.utc).isoformat(),
            "source_topic": _SOURCE_TOPIC,
            "error": error_msg,
            "error_type": error_type,
            "original_event": {"events": events},
        }
        self.logger.error(
            "sending events to DLQ: %s",
            error_msg,
            extra={"correlation_id": correlation_id},
        )
        if self.bus is not None:
            self.bus.publish(_DLQ_TOPIC, dlq_event)