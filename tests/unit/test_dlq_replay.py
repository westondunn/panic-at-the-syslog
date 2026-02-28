from __future__ import annotations

from libs.adapters.bus.in_memory import InMemoryBus
from tools.dlq_replay import replay


def _dlq_envelope(dlq_id: str = "dlq-001", original: dict | None = None) -> dict:
    return {
        "schema_version": "1.0",
        "dlq_id": dlq_id,
        "correlation_id": "corr-001",
        "failed_at": "2026-01-15T10:00:05Z",
        "source_topic": "events.normalized.v1",
        "error": "error in rule detect_brute_force: kaboom",
        "error_type": "rule_error",
        "original_event": original or {"events": [{"event_id": "evt-1"}]},
    }


# -- replay basic behaviour ---------------------------------------------------


def test_replay_publishes_original_events_to_target() -> None:
    bus = InMemoryBus()
    bus.publish("dlq.detector.v1", _dlq_envelope())

    replayed = replay(bus, "dlq.detector.v1", "events.normalized.v1")

    assert len(replayed) == 1
    target = bus.consume("events.normalized.v1")
    assert len(target) == 1
    assert target[0] == {"events": [{"event_id": "evt-1"}]}


def test_replay_returns_empty_when_dlq_is_empty() -> None:
    bus = InMemoryBus()
    replayed = replay(bus, "dlq.detector.v1", "events.normalized.v1")
    assert replayed == []


def test_replay_skips_entries_without_original_event() -> None:
    bus = InMemoryBus()
    bad_envelope = {
        "schema_version": "1.0",
        "dlq_id": "dlq-bad",
        "error": "oops",
    }
    bus.publish("dlq.detector.v1", bad_envelope)

    replayed = replay(bus, "dlq.detector.v1", "events.normalized.v1")

    assert replayed == []
    assert bus.consume("events.normalized.v1") == []


def test_replay_handles_multiple_messages() -> None:
    bus = InMemoryBus()
    bus.publish("dlq.detector.v1", _dlq_envelope("dlq-1", {"a": 1}))
    bus.publish("dlq.detector.v1", _dlq_envelope("dlq-2", {"b": 2}))

    replayed = replay(bus, "dlq.detector.v1", "events.normalized.v1")

    assert len(replayed) == 2
    target = bus.consume("events.normalized.v1")
    assert len(target) == 2


# -- dry-run mode --------------------------------------------------------------


def test_replay_dry_run_does_not_publish() -> None:
    bus = InMemoryBus()
    bus.publish("dlq.detector.v1", _dlq_envelope())

    replayed = replay(bus, "dlq.detector.v1", "events.normalized.v1", dry_run=True)

    assert len(replayed) == 1
    assert bus.consume("events.normalized.v1") == []
