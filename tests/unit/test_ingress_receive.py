"""Unit tests for IngressService.receive_syslog_line."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

from libs.adapters.bus import KafkaBusStub
from services.ingress.app import IngressService
from services.ingress.rate_limiter import TokenBucketRateLimiter


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_VALID_SYSLOG = "<13>Jan  5 15:33:03 myhost myapp[123]: test message"


class _FakeSpool:
    """Minimal SpoolWriter stand-in."""

    def __init__(self) -> None:
        self.messages: list[dict[str, Any]] = []

    def write(self, message: dict[str, Any]) -> None:
        self.messages.append(message)


# ---------------------------------------------------------------------------
# Constructor backward-compat
# ---------------------------------------------------------------------------


class TestConstructorCompat:
    def test_positional_bus(self) -> None:
        bus = KafkaBusStub()
        svc = IngressService(bus)
        assert svc.health()["service"] == "ingress"

    def test_keyword_bus(self) -> None:
        bus = KafkaBusStub()
        svc = IngressService(bus=bus)
        assert svc.health()["service"] == "ingress"

    def test_all_optional_kwargs(self) -> None:
        bus = KafkaBusStub()
        spool = _FakeSpool()
        rl = TokenBucketRateLimiter(rate=10.0, burst=10)
        svc = IngressService(bus, spool=spool, rate_limiter=rl, max_line_length=4096)
        assert svc._max_line_length == 4096


# ---------------------------------------------------------------------------
# receive_syslog_line – happy path
# ---------------------------------------------------------------------------


class TestReceiveSyslogLine:
    def test_returns_event_with_required_fields(self) -> None:
        bus = KafkaBusStub()
        svc = IngressService(bus)

        result = svc.receive_syslog_line(_VALID_SYSLOG)

        assert result is not None
        assert result["schema_version"] == "1.0"
        assert result["event_id"].startswith("evt-")
        assert result["correlation_id"].startswith("corr-")
        assert result["message"] == _VALID_SYSLOG
        assert result["received_at"].endswith("Z")
        assert "attributes" in result

    def test_source_from_parsed_hostname(self) -> None:
        bus = KafkaBusStub()
        svc = IngressService(bus)

        result = svc.receive_syslog_line(_VALID_SYSLOG, peer_address="10.0.0.1")

        assert result is not None
        assert result["source"] == "myhost"

    def test_source_falls_back_to_peer_address(self) -> None:
        bus = KafkaBusStub()
        svc = IngressService(bus)
        # Line without parseable hostname
        result = svc.receive_syslog_line("plain log line", peer_address="10.0.0.1")

        assert result is not None
        assert result["source"] == "10.0.0.1"

    def test_source_defaults_to_unknown(self) -> None:
        bus = KafkaBusStub()
        svc = IngressService(bus)

        result = svc.receive_syslog_line("plain log line")

        assert result is not None
        assert result["source"] == "unknown"

    def test_event_published_to_bus(self) -> None:
        bus = KafkaBusStub()
        svc = IngressService(bus)

        result = svc.receive_syslog_line(_VALID_SYSLOG)

        consumed = bus.consume("raw.syslog.v1")
        assert len(consumed) == 1
        assert consumed[0]["event_id"] == result["event_id"]

    def test_event_id_and_correlation_id_differ(self) -> None:
        bus = KafkaBusStub()
        svc = IngressService(bus)

        result = svc.receive_syslog_line(_VALID_SYSLOG)

        assert result is not None
        assert result["event_id"] != result["correlation_id"]

    def test_attributes_include_parsed_fields(self) -> None:
        bus = KafkaBusStub()
        svc = IngressService(bus)

        result = svc.receive_syslog_line(_VALID_SYSLOG)

        assert result is not None
        attrs = result["attributes"]
        assert attrs["facility"] == "user"
        assert attrs["severity"] == "notice"
        assert attrs["hostname"] == "myhost"
        assert attrs["program"] == "myapp"
        assert attrs["pid"] == 123


# ---------------------------------------------------------------------------
# receive_syslog_line – rate limiter
# ---------------------------------------------------------------------------


class TestRateLimiting:
    def test_returns_none_when_rate_limited(self) -> None:
        bus = KafkaBusStub()
        rl = MagicMock(spec=TokenBucketRateLimiter)
        rl.allow.return_value = False
        svc = IngressService(bus, rate_limiter=rl)

        result = svc.receive_syslog_line(_VALID_SYSLOG)

        assert result is None
        # Nothing published
        assert bus.consume("raw.syslog.v1") == []

    def test_proceeds_when_rate_limiter_allows(self) -> None:
        bus = KafkaBusStub()
        rl = MagicMock(spec=TokenBucketRateLimiter)
        rl.allow.return_value = True
        svc = IngressService(bus, rate_limiter=rl)

        result = svc.receive_syslog_line(_VALID_SYSLOG)

        assert result is not None

    def test_no_rate_limiter_always_proceeds(self) -> None:
        bus = KafkaBusStub()
        svc = IngressService(bus)

        result = svc.receive_syslog_line(_VALID_SYSLOG)

        assert result is not None


# ---------------------------------------------------------------------------
# receive_syslog_line – spool
# ---------------------------------------------------------------------------


class TestSpool:
    def test_writes_to_spool_when_provided(self) -> None:
        bus = KafkaBusStub()
        spool = _FakeSpool()
        svc = IngressService(bus, spool=spool)

        result = svc.receive_syslog_line(_VALID_SYSLOG)

        assert len(spool.messages) == 1
        assert spool.messages[0]["event_id"] == result["event_id"]

    def test_skips_spool_when_none(self) -> None:
        bus = KafkaBusStub()
        svc = IngressService(bus)

        result = svc.receive_syslog_line(_VALID_SYSLOG)

        # No exception, event still returned
        assert result is not None


# ---------------------------------------------------------------------------
# receive_syslog_line – validation errors propagate
# ---------------------------------------------------------------------------


class TestValidation:
    def test_empty_line_raises(self) -> None:
        bus = KafkaBusStub()
        svc = IngressService(bus)

        with pytest.raises(Exception, match="empty"):
            svc.receive_syslog_line("")

    def test_line_exceeding_max_length_raises(self) -> None:
        bus = KafkaBusStub()
        svc = IngressService(bus, max_line_length=10)

        with pytest.raises(Exception, match="max length"):
            svc.receive_syslog_line("x" * 11)
