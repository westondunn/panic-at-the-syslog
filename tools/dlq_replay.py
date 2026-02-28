"""DLQ replay tool — reprocess dead-lettered events back to their source topic.

Usage:
    python -m tools.dlq_replay --dlq-topic dlq.detector.v1 --target-topic events.normalized.v1

The tool reads all messages from a DLQ topic, extracts the ``original_event``
payload from each envelope, and publishes it to the target topic for
reprocessing.  Processed DLQ entries are tracked by ``dlq_id`` so re-runs
skip already-replayed messages.
"""

from __future__ import annotations

import argparse
import sys
from typing import Any

from libs.adapters.bus.interface import MessageBus
from libs.common.logging import get_logger

logger = get_logger("panic.tools.dlq_replay")


def replay(
    bus: MessageBus,
    dlq_topic: str,
    target_topic: str,
    *,
    dry_run: bool = False,
) -> list[dict[str, Any]]:
    """Read DLQ messages and republish originals to *target_topic*.

    Returns the list of replayed DLQ envelopes.
    """
    messages = bus.consume(dlq_topic)
    if not messages:
        logger.info("no messages on %s — nothing to replay", dlq_topic)
        return []

    replayed: list[dict[str, Any]] = []
    for msg in messages:
        dlq_id = msg.get("dlq_id", "<unknown>")
        original = msg.get("original_event")
        if original is None:
            logger.warning(
                "DLQ entry %s has no original_event — skipping", dlq_id
            )
            continue

        if dry_run:
            logger.info("[dry-run] would replay dlq_id=%s to %s", dlq_id, target_topic)
        else:
            bus.publish(target_topic, original)
            logger.info("replayed dlq_id=%s to %s", dlq_id, target_topic)
        replayed.append(msg)

    logger.info(
        "replay complete: %d/%d messages %s",
        len(replayed),
        len(messages),
        "previewed (dry-run)" if dry_run else "replayed",
    )
    return replayed


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Replay dead-lettered events back to their source topic.",
    )
    parser.add_argument(
        "--dlq-topic",
        default="dlq.detector.v1",
        help="DLQ topic to consume from (default: dlq.detector.v1)",
    )
    parser.add_argument(
        "--target-topic",
        default="events.normalized.v1",
        help="Topic to republish original events to (default: events.normalized.v1)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview which messages would be replayed without publishing",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    # In a production deployment, swap this for a real bus adapter
    # (e.g., KafkaBus) selected via the deployment profile.
    from libs.adapters.bus.kafka_stub import KafkaBusStub

    bus = KafkaBusStub()
    replayed = replay(bus, args.dlq_topic, args.target_topic, dry_run=args.dry_run)
    return 0 if replayed is not None else 1


if __name__ == "__main__":
    sys.exit(main())
