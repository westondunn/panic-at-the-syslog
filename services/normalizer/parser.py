from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any


_RE_SSH_AUTH = re.compile(
    r"(?P<action>Accepted|Failed) (?P<method>password|publickey) for (?P<user>\S+) from (?P<ip>\S+)"
)
_RE_FIREWALL = re.compile(
    r"(?P<action>DROP|ACCEPT)\s+(?:IN=(?P<iface>\S*))?\s*.*?SRC=(?P<src>\S+)\s+DST=(?P<dst>\S+)(?:.*?PROTO=(?P<proto>\S+))?"
)
_RE_DHCP = re.compile(
    r"DHCPACK\s+on\s+(?P<ip>\S+)\s+to\s+(?P<mac>[0-9a-fA-F:]+)(?:\s+\((?P<hostname>[^)]+)\))?(?:\s+via\s+\S+)?"
)
_RE_WAN = re.compile(
    r"(?P<iface>(?:eth|ppp)\S*)\s+link\s+(?P<state>up|down)"
)
_RE_LOGIN_FAIL = re.compile(
    r"(?i)login\s+failure.*?from\s+(?P<ip>\S+)"
)
_RE_IPV4 = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
_RE_MAC = re.compile(r"\b[0-9a-fA-F]{2}(?::[0-9a-fA-F]{2}){5}\b")

_VALID_SEVERITIES = frozenset({"debug", "info", "warn", "error", "critical"})


@dataclass(frozen=True)
class DeviceHint:
    ip: str | None
    mac: str | None
    hostname: str | None


@dataclass(frozen=True)
class NormalizedEvent:
    schema_version: str
    event_id: str
    correlation_id: str
    normalized_at: str
    source_device: str
    severity: str
    summary: str
    labels: list[str]

    def to_event(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "event_id": self.event_id,
            "correlation_id": self.correlation_id,
            "normalized_at": self.normalized_at,
            "source_device": self.source_device,
            "severity": self.severity,
            "summary": self.summary,
            "labels": list(self.labels),
        }


def extract_device_hint(message: str) -> DeviceHint:
    ip_match = _RE_IPV4.search(message)
    mac_match = _RE_MAC.search(message)
    return DeviceHint(
        ip=ip_match.group(0) if ip_match else None,
        mac=mac_match.group(0) if mac_match else None,
        hostname=None,
    )


def parse(raw: dict[str, Any]) -> NormalizedEvent:
    event_id: str = raw["event_id"]
    correlation_id: str = raw["correlation_id"]
    source: str = raw["source"]
    message: str = raw["message"]
    attributes: dict[str, Any] = raw.get("attributes", {})
    normalized_at = datetime.now(UTC).isoformat().replace("+00:00", "Z")

    severity: str
    summary: str
    labels: list[str]

    m = _RE_SSH_AUTH.search(message)
    if m:
        action = m.group("action")
        severity = "info" if action == "Accepted" else "warn"
        summary = f"SSH {action} for user '{m.group('user')}' via {m.group('method')} from {m.group('ip')}"
        labels = ["auth", "ssh", "synology"]
        return _build(event_id, correlation_id, normalized_at, source, severity, summary, labels)

    m = _RE_FIREWALL.search(message)
    if m:
        action = m.group("action")
        severity = "warn" if action == "DROP" else "info"
        proto = m.group("proto") or ""
        summary = f"Firewall {action} {proto} {m.group('src')} -> {m.group('dst')}"
        labels = ["firewall", "synology"]
        return _build(event_id, correlation_id, normalized_at, source, severity, summary, labels)

    m = _RE_DHCP.search(message)
    if m:
        severity = "info"
        summary = f"DHCP lease {m.group('ip')} to {m.group('mac')}"
        hostname = m.group("hostname")
        if hostname:
            summary = f"{summary} ({hostname})"
        labels = ["dhcp", "synology"]
        return _build(event_id, correlation_id, normalized_at, source, severity, summary, labels)

    m = _RE_WAN.search(message)
    if m:
        state = m.group("state")
        severity = "error" if state == "down" else "info"
        summary = f"WAN link {state} on {m.group('iface')}"
        labels = ["wan", "synology"]
        return _build(event_id, correlation_id, normalized_at, source, severity, summary, labels)

    m = _RE_LOGIN_FAIL.search(message)
    if m:
        severity = "warn"
        summary = f"Login failure from {m.group('ip')}"
        labels = ["auth", "synology"]
        return _build(event_id, correlation_id, normalized_at, source, severity, summary, labels)

    raw_severity = attributes.get("severity", "info")
    severity = raw_severity if raw_severity in _VALID_SEVERITIES else "info"
    summary = message[:80]
    labels = ["unclassified", "synology"]
    return _build(event_id, correlation_id, normalized_at, source, severity, summary, labels)


def _build(
    event_id: str,
    correlation_id: str,
    normalized_at: str,
    source_device: str,
    severity: str,
    summary: str,
    labels: list[str],
) -> NormalizedEvent:
    return NormalizedEvent(
        schema_version="1.0",
        event_id=event_id,
        correlation_id=correlation_id,
        normalized_at=normalized_at,
        source_device=source_device,
        severity=severity,
        summary=summary,
        labels=labels,
    )
