from __future__ import annotations


from libs.adapters.bus.in_memory import InMemoryBus
from services.detector.app import DetectorService
from services.detector.models import Finding
from services.detector.rules import (
    detect_brute_force,
    detect_dhcp_churn,
    detect_firewall_denies,
    detect_wan_flaps,
)


def _auth_event(event_id: str, device: str = "router-a", severity: str = "warn") -> dict:
    return {
        "schema_version": "1.0",
        "event_id": event_id,
        "correlation_id": "corr-001",
        "normalized_at": "2026-01-15T10:00:00Z",
        "source_device": device,
        "severity": severity,
        "summary": "Failed password for admin from 192.0.2.10",
        "labels": ["auth", "router"],
    }


def _wan_event(event_id: str, device: str = "router-a", direction: str = "down") -> dict:
    return {
        "schema_version": "1.0",
        "event_id": event_id,
        "correlation_id": "corr-wan-001",
        "normalized_at": "2026-01-15T10:00:00Z",
        "source_device": device,
        "severity": "warn",
        "summary": f"WAN link {direction} detected",
        "labels": ["wan", "link"],
    }


def _firewall_event(event_id: str, device: str = "firewall-a") -> dict:
    return {
        "schema_version": "1.0",
        "event_id": event_id,
        "correlation_id": "corr-fw-001",
        "normalized_at": "2026-01-15T10:00:00Z",
        "source_device": device,
        "severity": "warn",
        "summary": "Denied TCP 192.0.2.50:44321 -> 10.0.0.1:22",
        "labels": ["firewall"],
    }


def _dhcp_event(event_id: str, device: str = "router-a") -> dict:
    return {
        "schema_version": "1.0",
        "event_id": event_id,
        "correlation_id": "corr-dhcp-001",
        "normalized_at": "2026-01-15T10:00:00Z",
        "source_device": device,
        "severity": "info",
        "summary": "DHCP lease assigned to 00:11:22:33:44:55",
        "labels": ["dhcp"],
    }


# -- Finding model tests -------------------------------------------------------


def test_finding_to_event_includes_schema_version() -> None:
    finding = Finding(
        finding_id="find-test",
        correlation_id="corr-001",
        detected_at="2026-01-15T10:00:00Z",
        category="brute-force-suspected",
        confidence=0.8,
        severity="high",
        evidence=[],
        details={},
    )
    event = finding.to_event()
    assert event["schema_version"] == "1.0"
    assert event["finding_id"] == "find-test"
    assert event["severity"] == "high"
    assert event["evidence"] == []


# -- Brute force detection tests ------------------------------------------------


def test_detect_brute_force_triggers_at_threshold() -> None:
    events = [_auth_event(f"evt-{i}") for i in range(5)]
    findings = detect_brute_force(events)
    assert len(findings) == 1
    assert findings[0].category == "brute-force-suspected"
    assert findings[0].details["attempts"] == 5


def test_detect_brute_force_no_trigger_below_threshold() -> None:
    events = [_auth_event(f"evt-{i}") for i in range(4)]
    findings = detect_brute_force(events)
    assert len(findings) == 0


def test_detect_brute_force_ignores_info_severity() -> None:
    events = [_auth_event(f"evt-{i}", severity="info") for i in range(10)]
    findings = detect_brute_force(events)
    assert len(findings) == 0


def test_detect_brute_force_confidence_scales() -> None:
    events = [_auth_event(f"evt-{i}") for i in range(10)]
    findings = detect_brute_force(events)
    assert findings[0].confidence == 1.0


def test_detect_brute_force_groups_by_device() -> None:
    events = [_auth_event(f"evt-a-{i}", device="router-a") for i in range(5)]
    events += [_auth_event(f"evt-b-{i}", device="router-b") for i in range(3)]
    findings = detect_brute_force(events)
    assert len(findings) == 1
    assert findings[0].details["source_device"] == "router-a"


# -- WAN flap detection tests --------------------------------------------------


def test_detect_wan_flaps_triggers_at_threshold() -> None:
    events = [
        _wan_event("evt-1", direction="down"),
        _wan_event("evt-2", direction="up"),
        _wan_event("evt-3", direction="down"),
    ]
    findings = detect_wan_flaps(events)
    assert len(findings) == 1
    assert findings[0].category == "wan-instability"
    assert findings[0].details["flap_count"] == 3


def test_detect_wan_flaps_no_trigger_below_threshold() -> None:
    events = [_wan_event("evt-1"), _wan_event("evt-2")]
    findings = detect_wan_flaps(events)
    assert len(findings) == 0


# -- Firewall deny detection tests ---------------------------------------------


def test_detect_firewall_denies_triggers_at_threshold() -> None:
    events = [_firewall_event(f"evt-{i}") for i in range(10)]
    findings = detect_firewall_denies(events)
    assert len(findings) == 1
    assert findings[0].category == "firewall-deny-flood"
    assert findings[0].details["deny_count"] == 10


def test_detect_firewall_denies_no_trigger_below_threshold() -> None:
    events = [_firewall_event(f"evt-{i}") for i in range(9)]
    findings = detect_firewall_denies(events)
    assert len(findings) == 0


# -- DHCP churn detection tests ------------------------------------------------


def test_detect_dhcp_churn_triggers_at_threshold() -> None:
    events = [_dhcp_event(f"evt-{i}") for i in range(5)]
    findings = detect_dhcp_churn(events)
    assert len(findings) == 1
    assert findings[0].category == "dhcp-churn"
    assert findings[0].details["churn_count"] == 5


def test_detect_dhcp_churn_no_trigger_below_threshold() -> None:
    events = [_dhcp_event(f"evt-{i}") for i in range(4)]
    findings = detect_dhcp_churn(events)
    assert len(findings) == 0


# -- Idempotency tests ---------------------------------------------------------


def test_finding_id_is_deterministic() -> None:
    events = [_auth_event(f"evt-{i}") for i in range(5)]
    findings_1 = detect_brute_force(events)
    findings_2 = detect_brute_force(events)
    assert findings_1[0].finding_id == findings_2[0].finding_id


def test_finding_id_stable_regardless_of_event_order() -> None:
    events_a = [_auth_event(f"evt-{i}") for i in range(5)]
    events_b = list(reversed(events_a))
    findings_a = detect_brute_force(events_a)
    findings_b = detect_brute_force(events_b)
    assert findings_a[0].finding_id == findings_b[0].finding_id


def test_different_events_produce_different_finding_ids() -> None:
    events_a = [_auth_event(f"evt-a-{i}") for i in range(5)]
    events_b = [_auth_event(f"evt-b-{i}") for i in range(5)]
    findings_a = detect_brute_force(events_a)
    findings_b = detect_brute_force(events_b)
    assert findings_a[0].finding_id != findings_b[0].finding_id


# -- DetectorService integration tests -----------------------------------------


def test_process_publishes_findings_to_bus() -> None:
    bus = InMemoryBus()
    svc = DetectorService(bus=bus)
    events = [_auth_event(f"evt-{i}") for i in range(5)]

    result = svc.process(events)

    published = bus.consume("findings.realtime.v1")
    assert len(published) == 1
    assert len(result) == 1
    assert published[0]["category"] == "brute-force-suspected"
    assert published[0]["schema_version"] == "1.0"
    assert published[0]["severity"] in ("low", "medium", "high", "critical")
    assert isinstance(published[0]["evidence"], list)


def test_process_returns_empty_when_no_detections() -> None:
    bus = InMemoryBus()
    svc = DetectorService(bus=bus)
    events = [_auth_event("evt-1", severity="info")]

    result = svc.process(events)

    assert result == []
    assert bus.consume("findings.realtime.v1") == []


def test_process_without_bus_does_not_raise() -> None:
    svc = DetectorService(bus=None)
    events = [_auth_event(f"evt-{i}") for i in range(5)]
    result = svc.process(events)
    assert len(result) == 1


def test_process_handles_multiple_rule_matches() -> None:
    bus = InMemoryBus()
    svc = DetectorService(bus=bus)
    events = [_auth_event(f"evt-auth-{i}") for i in range(5)]
    events += [_dhcp_event(f"evt-dhcp-{i}") for i in range(5)]

    result = svc.process(events)

    assert len(result) == 2
    categories = {f["category"] for f in result}
    assert "brute-force-suspected" in categories
    assert "dhcp-churn" in categories


def test_process_idempotent_with_same_events() -> None:
    bus = InMemoryBus()
    svc = DetectorService(bus=bus)
    events = [_auth_event(f"evt-{i}") for i in range(5)]

    result_1 = svc.process(events)
    result_2 = svc.process(events)

    assert result_1[0]["finding_id"] == result_2[0]["finding_id"]


# -- Evidence pointer tests ----------------------------------------------------


def test_evidence_contains_event_references() -> None:
    events = [_auth_event(f"evt-{i}") for i in range(5)]
    findings = detect_brute_force(events)

    evidence = findings[0].evidence
    assert len(evidence) == 5
    for item in evidence:
        assert "event_id" in item
        assert "source_device" in item
        assert "summary" in item


# -- Severity mapping tests ----------------------------------------------------


def test_severity_derives_from_confidence() -> None:
    events_5 = [_auth_event(f"evt-{i}") for i in range(5)]
    findings = detect_brute_force(events_5)
    assert findings[0].severity == "medium"

    events_7 = [_auth_event(f"evt-{i}") for i in range(7)]
    findings = detect_brute_force(events_7)
    assert findings[0].severity == "high"

    events_10 = [_auth_event(f"evt-{i}") for i in range(10)]
    findings = detect_brute_force(events_10)
    assert findings[0].severity == "critical"


# -- Correlation ID propagation test -------------------------------------------


def test_correlation_id_propagated_from_events() -> None:
    events = [_auth_event(f"evt-{i}") for i in range(5)]
    findings = detect_brute_force(events)
    assert findings[0].correlation_id == "corr-001"
