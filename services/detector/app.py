from __future__ import annotations

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


class DetectorService:
    def __init__(self, bus: MessageBus | None = None) -> None:
        self.bus = bus
        self.logger = get_logger("panic.services.detector")

    def health(self) -> dict[str, str]:
        return {"status": "ok", "service": "detector"}

    def process(self, events: list[dict[str, Any]]) -> list[dict[str, Any]]:
        all_findings: list[dict[str, Any]] = []
        for rule in _RULES:
            for finding in rule(events):
                finding_event = finding.to_event()
                all_findings.append(finding_event)
                self.logger.info(
                    "finding detected: %s",
                    finding.category,
                    extra={"correlation_id": finding.correlation_id},
                )
                if self.bus is not None:
                    self.bus.publish("findings.realtime.v1", finding_event)
        return all_findings