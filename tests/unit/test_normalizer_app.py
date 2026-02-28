from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from libs.common.errors import ValidationError
from services.normalizer.app import NormalizerService
from services.normalizer.parser import NormalizedEvent


def _valid_raw_event() -> dict:
    return {
        "schema_version": "1.0",
        "event_id": "evt-123",
        "correlation_id": "corr-456",
        "source": "synology-nas",
        "received_at": "2025-01-01T00:00:00Z",
        "message": "Accepted publickey for admin from 192.168.1.10",
    }


# -- normalize ----------------------------------------------------------------


def test_normalize_returns_normalized_event() -> None:
    svc = NormalizerService()
    result = svc.normalize(_valid_raw_event())

    assert isinstance(result, NormalizedEvent)
    assert result.event_id == "evt-123"
    assert result.correlation_id == "corr-456"
    assert result.source_device == "synology-nas"


def test_normalize_raises_on_missing_keys() -> None:
    raw = {"schema_version": "1.0", "event_id": "evt-123"}
    svc = NormalizerService()

    with pytest.raises(ValidationError, match="missing required keys"):
        svc.normalize(raw)

    # Verify the error mentions specific missing key names.
    try:
        svc.normalize(raw)
    except ValidationError as exc:
        msg = str(exc)
        for key in ("correlation_id", "message", "received_at", "source"):
            assert key in msg


def test_normalize_without_bus_works() -> None:
    svc = NormalizerService(bus=None)
    result = svc.normalize(_valid_raw_event())

    assert isinstance(result, NormalizedEvent)


# -- process ------------------------------------------------------------------


def test_process_publishes_to_normalized_topic() -> None:
    bus = MagicMock()
    svc = NormalizerService(bus=bus)

    svc.process(_valid_raw_event())

    bus.publish.assert_called_once()
    topic, payload = bus.publish.call_args[0]
    assert topic == "events.normalized.v1"
    assert isinstance(payload, dict)


def test_process_publishes_to_dlq_on_validation_error() -> None:
    bus = MagicMock()
    svc = NormalizerService(bus=bus)
    raw = {"schema_version": "1.0"}  # missing several required keys

    svc.process(raw)

    bus.publish.assert_called_once()
    topic, payload = bus.publish.call_args[0]
    assert topic == "dlq.normalizer.v1"
    assert payload["error_type"] == "validation"
    assert payload["original_event"] is raw


@patch("services.normalizer.app.parse", side_effect=RuntimeError("boom"))
def test_process_publishes_to_dlq_on_unexpected_error(_mock_parse: MagicMock) -> None:
    bus = MagicMock()
    svc = NormalizerService(bus=bus)

    svc.process(_valid_raw_event())

    bus.publish.assert_called_once()
    topic, payload = bus.publish.call_args[0]
    assert topic == "dlq.normalizer.v1"
    assert payload["error_type"] == "unexpected"
    assert "boom" in payload["error"]


def test_process_without_bus_does_not_raise() -> None:
    svc = NormalizerService(bus=None)
    # Should complete without raising, even though there is no bus to publish to.
    svc.process(_valid_raw_event())
