from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

from libs.adapters.bus.interface import MessageBus
from libs.adapters.spool.interface import SpoolWriter
from libs.common.logging import get_logger
from services.ingress.rate_limiter import TokenBucketRateLimiter
from services.ingress.syslog_parser import parse_syslog_line


class IngressService:
    def __init__(
        self,
        bus: MessageBus,
        *,
        spool: SpoolWriter | None = None,
        rate_limiter: TokenBucketRateLimiter | None = None,
        max_line_length: int = 8192,
    ) -> None:
        self.bus = bus
        self.logger = get_logger("panic.services.ingress")
        self._spool = spool
        self._rate_limiter = rate_limiter
        self._max_line_length = max_line_length

    def health(self) -> dict[str, str]:
        return {"status": "ok", "service": "ingress"}

    def publish_raw_event(self, event: dict[str, object]) -> None:
        self.logger.info("publishing raw event", extra={"event_id": event.get("event_id")})
        self.bus.publish("raw.syslog.v1", event)

    def receive_syslog_line(
        self,
        line: str,
        *,
        peer_address: str = "unknown",
    ) -> dict[str, Any] | None:
        """Parse a syslog line, build a raw event, publish it, and return it.

        Returns ``None`` when the call is rejected by the rate limiter.
        """
        if self._rate_limiter is not None and not self._rate_limiter.allow():
            self.logger.warning(
                "rate-limited syslog line",
                extra={"peer_address": peer_address},
            )
            return None

        parsed = parse_syslog_line(line, max_length=self._max_line_length)

        event_hex = uuid.uuid4().hex[:12]
        corr_hex = uuid.uuid4().hex[:12]

        source = parsed["attributes"].get("hostname") or peer_address

        event: dict[str, Any] = {
            "schema_version": "1.0",
            "event_id": f"evt-{event_hex}",
            "correlation_id": f"corr-{corr_hex}",
            "source": source,
            "received_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
            "message": line,
            "attributes": parsed["attributes"],
        }

        if self._spool is not None:
            self._spool.write(event)

        self.publish_raw_event(event)
        return event