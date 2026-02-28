from __future__ import annotations

from collections import defaultdict
from datetime import UTC, datetime
from hashlib import sha256
from typing import Any

from .models import Finding


def _severity_from_confidence(confidence: float) -> str:
    if confidence >= 0.9:
        return "critical"
    if confidence >= 0.7:
        return "high"
    if confidence >= 0.5:
        return "medium"
    return "low"


def _build_finding_id(category: str, key: str, event_ids: list[str]) -> str:
    stable_ids = ":".join(sorted(event_ids))
    digest = sha256(
        f"{category}:{key}:{stable_ids}".encode("utf-8")
    ).hexdigest()[:16]
    return f"find-{digest}"


def _build_evidence(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "event_id": evt.get("event_id", ""),
            "source_device": evt.get("source_device", ""),
            "summary": evt.get("summary", ""),
        }
        for evt in events
    ]


def _group_by_source_device(
    events: list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for evt in events:
        device = evt.get("source_device", "unknown")
        groups[device].append(evt)
    return groups


def detect_brute_force(events: list[dict[str, Any]]) -> list[Finding]:
    matched = [
        evt
        for evt in events
        if "auth" in evt.get("labels", [])
        and evt.get("severity") in ("warn", "error")
    ]
    findings: list[Finding] = []
    for device, group in _group_by_source_device(matched).items():
        if len(group) < 5:
            continue
        event_ids = [e.get("event_id", "") for e in group]
        confidence = min(len(group) / 10, 1.0)
        finding_id = _build_finding_id("brute-force-suspected", device, event_ids)
        findings.append(
            Finding(
                finding_id=finding_id,
                correlation_id=group[0].get("correlation_id", ""),
                detected_at=datetime.now(UTC).isoformat().replace("+00:00", "Z"),
                category="brute-force-suspected",
                confidence=confidence,
                severity=_severity_from_confidence(confidence),
                evidence=_build_evidence(group),
                details={"source_device": device, "attempts": len(group)},
            )
        )
    return findings


def detect_wan_flaps(events: list[dict[str, Any]]) -> list[Finding]:
    matched = [
        evt
        for evt in events
        if (
            {"wan", "link"} & set(evt.get("labels", []))
            and any(
                kw in evt.get("summary", "").lower() for kw in ("up", "down")
            )
        )
    ]
    findings: list[Finding] = []
    for device, group in _group_by_source_device(matched).items():
        if len(group) < 3:
            continue
        event_ids = [e.get("event_id", "") for e in group]
        confidence = min(len(group) / 6, 1.0)
        finding_id = _build_finding_id("wan-instability", device, event_ids)
        findings.append(
            Finding(
                finding_id=finding_id,
                correlation_id=group[0].get("correlation_id", ""),
                detected_at=datetime.now(UTC).isoformat().replace("+00:00", "Z"),
                category="wan-instability",
                confidence=confidence,
                severity=_severity_from_confidence(confidence),
                evidence=_build_evidence(group),
                details={"source_device": device, "flap_count": len(group)},
            )
        )
    return findings


def detect_firewall_denies(events: list[dict[str, Any]]) -> list[Finding]:
    matched = [
        evt
        for evt in events
        if "firewall" in evt.get("labels", [])
        and evt.get("severity") in ("warn", "error")
    ]
    findings: list[Finding] = []
    for device, group in _group_by_source_device(matched).items():
        if len(group) < 10:
            continue
        event_ids = [e.get("event_id", "") for e in group]
        confidence = min(len(group) / 20, 1.0)
        finding_id = _build_finding_id("firewall-deny-flood", device, event_ids)
        findings.append(
            Finding(
                finding_id=finding_id,
                correlation_id=group[0].get("correlation_id", ""),
                detected_at=datetime.now(UTC).isoformat().replace("+00:00", "Z"),
                category="firewall-deny-flood",
                confidence=confidence,
                severity=_severity_from_confidence(confidence),
                evidence=_build_evidence(group),
                details={"source_device": device, "deny_count": len(group)},
            )
        )
    return findings


def detect_dhcp_churn(events: list[dict[str, Any]]) -> list[Finding]:
    matched = [
        evt for evt in events if "dhcp" in evt.get("labels", [])
    ]
    findings: list[Finding] = []
    for device, group in _group_by_source_device(matched).items():
        if len(group) < 5:
            continue
        event_ids = [e.get("event_id", "") for e in group]
        confidence = min(len(group) / 10, 1.0)
        finding_id = _build_finding_id("dhcp-churn", device, event_ids)
        findings.append(
            Finding(
                finding_id=finding_id,
                correlation_id=group[0].get("correlation_id", ""),
                detected_at=datetime.now(UTC).isoformat().replace("+00:00", "Z"),
                category="dhcp-churn",
                confidence=confidence,
                severity=_severity_from_confidence(confidence),
                evidence=_build_evidence(group),
                details={"source_device": device, "churn_count": len(group)},
            )
        )
    return findings
