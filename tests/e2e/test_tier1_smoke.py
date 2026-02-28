import pytest

from libs.adapters.bus import KafkaBusStub
from services.ingress.app import IngressService


@pytest.mark.e2e
def test_tier1_smoke_publish_and_consume() -> None:
    bus = KafkaBusStub()
    ingress = IngressService(bus=bus)
    event = {
        "schema_version": "1.0",
        "event_id": "evt-smoke-001",
        "correlation_id": "corr-smoke-001",
        "source": "router-smoke",
        "received_at": "2026-01-15T10:00:00Z",
        "message": "smoke event",
    }

    ingress.publish_raw_event(event)

    consumed = bus.consume("raw.syslog.v1")
    assert len(consumed) == 1
    assert consumed[0]["event_id"] == "evt-smoke-001"
