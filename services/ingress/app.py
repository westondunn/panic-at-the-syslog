from __future__ import annotations

from libs.adapters.bus.interface import MessageBus
from libs.common.logging import get_logger


class IngressService:
    def __init__(self, bus: MessageBus) -> None:
        self.bus = bus
        self.logger = get_logger("panic.services.ingress")

    def health(self) -> dict[str, str]:
        return {"status": "ok", "service": "ingress"}

    def publish_raw_event(self, event: dict[str, object]) -> None:
        self.logger.info("publishing raw event", extra={"event_id": event.get("event_id")})
        self.bus.publish("raw.syslog.v1", event)