from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema
import pytest

from services.normalizer.parser import (
    DeviceHint,
    extract_device_hint,
    parse,
)

_SCHEMA_PATH = (
    Path(__file__).resolve().parents[2]
    / "contracts"
    / "events"
    / "events.normalized.v1.schema.json"
)
_SCHEMA = json.loads(_SCHEMA_PATH.read_text())


def _raw(
    message: str,
    *,
    event_id: str = "evt-001",
    correlation_id: str = "corr-001",
    source: str = "router.local",
    attributes: dict[str, Any] | None = None,
) -> dict[str, Any]:
    d: dict[str, Any] = {
        "event_id": event_id,
        "correlation_id": correlation_id,
        "source": source,
        "message": message,
    }
    if attributes is not None:
        d["attributes"] = attributes
    return d


def _assert_schema_valid(event: dict[str, Any]) -> None:
    jsonschema.validate(instance=event, schema=_SCHEMA)


# --- SSH Auth ---


def test_ssh_accepted() -> None:
    result = parse(_raw("Accepted publickey for admin from 10.0.0.5"))
    assert result.severity == "info"
    assert result.summary == "SSH Accepted for user 'admin' via publickey from 10.0.0.5"
    assert result.labels == ["auth", "ssh", "synology"]
    _assert_schema_valid(result.to_event())


def test_ssh_failed() -> None:
    result = parse(_raw("Failed password for root from 192.168.1.100"))
    assert result.severity == "warn"
    assert "Failed" in result.summary
    assert "root" in result.summary
    assert result.labels == ["auth", "ssh", "synology"]
    _assert_schema_valid(result.to_event())


# --- Firewall ---


def test_firewall_drop() -> None:
    msg = "DROP  IN=eth0 OUT= SRC=203.0.113.5 DST=10.0.0.1 PROTO=TCP"
    result = parse(_raw(msg))
    assert result.severity == "warn"
    assert "DROP" in result.summary
    assert "TCP" in result.summary
    assert "203.0.113.5" in result.summary
    assert result.labels == ["firewall", "synology"]
    _assert_schema_valid(result.to_event())


def test_firewall_accept() -> None:
    msg = "ACCEPT IN=eth1 SRC=10.0.0.2 DST=10.0.0.1 PROTO=UDP"
    result = parse(_raw(msg))
    assert result.severity == "info"
    assert "ACCEPT" in result.summary
    assert result.labels == ["firewall", "synology"]
    _assert_schema_valid(result.to_event())


def test_firewall_no_proto() -> None:
    msg = "DROP  IN=eth0 SRC=1.2.3.4 DST=5.6.7.8"
    result = parse(_raw(msg))
    assert result.severity == "warn"
    assert "1.2.3.4" in result.summary
    assert "5.6.7.8" in result.summary
    _assert_schema_valid(result.to_event())


# --- DHCP ---


def test_dhcp_with_hostname() -> None:
    msg = "DHCPACK on 192.168.1.50 to aa:bb:cc:dd:ee:ff (myphone) via eth0"
    result = parse(_raw(msg))
    assert result.severity == "info"
    assert "192.168.1.50" in result.summary
    assert "aa:bb:cc:dd:ee:ff" in result.summary
    assert "(myphone)" in result.summary
    assert result.labels == ["dhcp", "synology"]
    _assert_schema_valid(result.to_event())


def test_dhcp_without_hostname() -> None:
    msg = "DHCPACK on 10.0.0.42 to 11:22:33:44:55:66"
    result = parse(_raw(msg))
    assert result.severity == "info"
    assert "10.0.0.42" in result.summary
    assert "()" not in result.summary
    assert result.labels == ["dhcp", "synology"]
    _assert_schema_valid(result.to_event())


# --- WAN ---


def test_wan_link_down() -> None:
    result = parse(_raw("eth0 link down"))
    assert result.severity == "error"
    assert result.summary == "WAN link down on eth0"
    assert result.labels == ["wan", "synology"]
    _assert_schema_valid(result.to_event())


def test_wan_link_up() -> None:
    result = parse(_raw("ppp0 link up"))
    assert result.severity == "info"
    assert result.summary == "WAN link up on ppp0"
    assert result.labels == ["wan", "synology"]
    _assert_schema_valid(result.to_event())


# --- Login Failure ---


def test_login_failure() -> None:
    result = parse(_raw("Login failure for admin from 172.16.0.99"))
    assert result.severity == "warn"
    assert result.summary == "Login failure from 172.16.0.99"
    assert result.labels == ["auth", "synology"]
    _assert_schema_valid(result.to_event())


def test_login_failure_case_insensitive() -> None:
    result = parse(_raw("LOGIN FAILURE detected from 10.10.10.10"))
    assert result.severity == "warn"
    assert "10.10.10.10" in result.summary
    _assert_schema_valid(result.to_event())


# --- Fallback ---


def test_fallback_unclassified() -> None:
    result = parse(_raw("Some random syslog message we don't recognize"))
    assert result.severity == "info"
    assert result.labels == ["unclassified", "synology"]
    assert result.summary == "Some random syslog message we don't recognize"
    _assert_schema_valid(result.to_event())


def test_fallback_uses_attribute_severity() -> None:
    result = parse(
        _raw(
            "Unmapped event text",
            attributes={"severity": "error"},
        )
    )
    assert result.severity == "error"
    _assert_schema_valid(result.to_event())


def test_fallback_invalid_severity_defaults_to_info() -> None:
    result = parse(
        _raw(
            "Something happened",
            attributes={"severity": "bogus"},
        )
    )
    assert result.severity == "info"
    _assert_schema_valid(result.to_event())


def test_fallback_truncates_summary() -> None:
    long_msg = "x" * 200
    result = parse(_raw(long_msg))
    assert len(result.summary) == 80
    _assert_schema_valid(result.to_event())


# --- extract_device_hint ---


def test_extract_device_hint_ip_and_mac() -> None:
    hint = extract_device_hint("SRC=192.168.1.1 MAC=aa:bb:cc:dd:ee:ff")
    assert hint == DeviceHint(ip="192.168.1.1", mac="aa:bb:cc:dd:ee:ff", hostname=None)


def test_extract_device_hint_ip_only() -> None:
    hint = extract_device_hint("Connection from 10.0.0.1 port 22")
    assert hint.ip == "10.0.0.1"
    assert hint.mac is None
    assert hint.hostname is None


def test_extract_device_hint_no_match() -> None:
    hint = extract_device_hint("no addresses here")
    assert hint == DeviceHint(ip=None, mac=None, hostname=None)


# --- NormalizedEvent dataclass ---


def test_normalized_event_is_frozen() -> None:
    result = parse(_raw("eth0 link up"))
    with pytest.raises(AttributeError):
        result.severity = "debug"  # type: ignore[misc]


def test_to_event_matches_schema_fields() -> None:
    result = parse(_raw("Accepted password for admin from 10.0.0.5"))
    event = result.to_event()
    expected_keys = {
        "schema_version",
        "event_id",
        "correlation_id",
        "normalized_at",
        "source_device",
        "severity",
        "summary",
        "labels",
    }
    assert set(event.keys()) == expected_keys


def test_to_event_labels_is_new_list() -> None:
    result = parse(_raw("eth0 link up"))
    event = result.to_event()
    event["labels"].append("extra")
    assert "extra" not in result.labels


# --- Field propagation ---


def test_source_device_propagation() -> None:
    result = parse(_raw("anything", source="my-router"))
    assert result.source_device == "my-router"


def test_event_id_propagation() -> None:
    result = parse(_raw("anything", event_id="evt-abc"))
    assert result.event_id == "evt-abc"


def test_correlation_id_propagation() -> None:
    result = parse(_raw("anything", correlation_id="corr-xyz"))
    assert result.correlation_id == "corr-xyz"


def test_schema_version_is_1_0() -> None:
    result = parse(_raw("anything"))
    assert result.schema_version == "1.0"


def test_normalized_at_is_utc_iso() -> None:
    result = parse(_raw("anything"))
    assert result.normalized_at.endswith("Z")
    assert "+" not in result.normalized_at


# --- Regex priority ---


def test_ssh_takes_priority_over_login_failure() -> None:
    msg = "Failed password for root from 10.0.0.1 login failure from 10.0.0.1"
    result = parse(_raw(msg))
    assert result.labels == ["auth", "ssh", "synology"]
