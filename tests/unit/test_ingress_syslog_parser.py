"""Unit tests for services.ingress.syslog_parser.parse_syslog_line."""

from __future__ import annotations

import pytest

from libs.common.errors import ValidationError
from services.ingress.syslog_parser import parse_syslog_line


# ---------------------------------------------------------------------------
# Happy-path parsing
# ---------------------------------------------------------------------------


class TestParseValidRfc3164Line:
    """Basic PRI decoding with facility/severity."""

    def test_parse_valid_rfc3164_line(self) -> None:
        line = "<13>Jan  5 15:33:03 myhost myapp[123]: test message"
        result = parse_syslog_line(line)

        assert result["raw_message"] == line
        attrs = result["attributes"]
        assert attrs["priority"] == 13
        assert attrs["facility"] == "user"
        assert attrs["severity"] == "notice"
        assert attrs["hostname"] == "myhost"
        assert attrs["program"] == "myapp"
        assert attrs["pid"] == 123


# ---------------------------------------------------------------------------
# Synology-specific messages
# ---------------------------------------------------------------------------


class TestParseSynologyMessages:
    """Synology Router syslog samples."""

    def test_parse_synology_ufw_block(self) -> None:
        line = (
            "<134>Jan 15 10:05:23 SynologyRouter kernel: "
            "[UFW BLOCK] IN=eth0 OUT= MAC=00:11:32:xx:xx:xx "
            "SRC=198.51.100.42 DST=192.168.1.1 PROTO=TCP SPT=54321 DPT=443"
        )
        result = parse_syslog_line(line)

        attrs = result["attributes"]
        assert attrs["facility"] == "local0"
        assert attrs["severity"] == "info"
        assert attrs["priority"] == 134
        assert attrs["hostname"] == "SynologyRouter"
        assert attrs["program"] == "kernel"
        assert "pid" not in attrs

    def test_parse_synology_sshd_accepted(self) -> None:
        line = (
            "<86>Jan 15 10:05:23 SynologyRouter sshd[12345]: "
            "Accepted password for admin from 192.0.2.10"
        )
        result = parse_syslog_line(line)

        attrs = result["attributes"]
        assert attrs["facility"] == "authpriv"
        assert attrs["severity"] == "info"
        assert attrs["priority"] == 86
        assert attrs["hostname"] == "SynologyRouter"
        assert attrs["program"] == "sshd"
        assert attrs["pid"] == 12345


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_parse_no_pri_header(self) -> None:
        result = parse_syslog_line("plain log line without PRI")

        assert result["raw_message"] == "plain log line without PRI"
        assert result["attributes"] == {}


# ---------------------------------------------------------------------------
# Validation errors
# ---------------------------------------------------------------------------


class TestValidationErrors:
    def test_reject_empty_line(self) -> None:
        with pytest.raises(ValidationError, match="empty"):
            parse_syslog_line("")

    def test_reject_oversized_line(self) -> None:
        with pytest.raises(ValidationError, match="max length"):
            parse_syslog_line("x" * 100, max_length=50)

    def test_reject_invalid_pri_value(self) -> None:
        with pytest.raises(ValidationError, match="192"):
            parse_syslog_line("<192>some message")


# ---------------------------------------------------------------------------
# Facility / severity decoding truth table
# ---------------------------------------------------------------------------


class TestFacilitySeverityDecoding:
    """Verify specific PRI values decode to the correct facility/severity."""

    @pytest.mark.parametrize(
        ("pri", "facility", "severity"),
        [
            (0, "kern", "emerg"),
            (13, "user", "notice"),
            (34, "auth", "crit"),
            (86, "authpriv", "info"),
            (134, "local0", "info"),
            (165, "local4", "notice"),
            (191, "local7", "debug"),
        ],
        ids=[
            "pri-0-kern-emerg",
            "pri-13-user-notice",
            "pri-34-auth-crit",
            "pri-86-authpriv-info",
            "pri-134-local0-info",
            "pri-165-local4-notice",
            "pri-191-local7-debug",
        ],
    )
    def test_facility_severity_decoding(
        self, pri: int, facility: str, severity: str
    ) -> None:
        line = f"<{pri}>Jan  1 00:00:00 host prog: msg"
        result = parse_syslog_line(line)

        attrs = result["attributes"]
        assert attrs["priority"] == pri
        assert attrs["facility"] == facility
        assert attrs["severity"] == severity
