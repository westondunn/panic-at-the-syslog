from __future__ import annotations

from libs.adapters.bus.interface import MessageBus
from libs.common.errors import ValidationError
from libs.common.logging import get_logger

from .parser import NormalizedEvent, parse

_REQUIRED_KEYS = frozenset(
    {"schema_version", "event_id", "correlation_id", "source", "received_at", "message"}
)


class NormalizerService:
    def __init__(self, bus: MessageBus | None = None) -> None:
        self.bus = bus
        self.logger = get_logger("panic.services.normalizer")

    def health(self) -> dict[str, str]:
        return {"status": "ok", "service": "normalizer"}

    def normalize(self, raw_event: dict) -> NormalizedEvent:
        missing = _REQUIRED_KEYS - raw_event.keys()
        if missing:
            raise ValidationError(
                f"missing required keys: {', '.join(sorted(missing))}"
            )
        return parse(raw_event)

    def process(self, raw_event: dict) -> None:
        correlation_id = raw_event.get("correlation_id")
        try:
            result = self.normalize(raw_event)
            self.logger.info(
                "normalized event",
                extra={"correlation_id": correlation_id},
            )
            if self.bus is not None:
                self.bus.publish("events.normalized.v1", result.to_event())
        except ValidationError as exc:
            self.logger.warning(
                "validation error during normalization: %s",
                exc,
                extra={"correlation_id": correlation_id},
            )
            if self.bus is not None:
                self.bus.publish(
                    "dlq.normalizer.v1",
                    {
                        "original_event": raw_event,
                        "error": str(exc),
                        "error_type": "validation",
                    },
                )
        except Exception as exc:
            self.logger.error(
                "unexpected error during normalization: %s",
                exc,
                extra={"correlation_id": correlation_id},
            )
            if self.bus is not None:
                self.bus.publish(
                    "dlq.normalizer.v1",
                    {
                        "original_event": raw_event,
                        "error": str(exc),
                        "error_type": "unexpected",
                    },
                )