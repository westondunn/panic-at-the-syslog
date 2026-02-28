"""CLI entrypoint for the ingress service (``python -m services.ingress``)."""

from __future__ import annotations

import asyncio

from libs.adapters.bus.kafka_stub import KafkaBusStub
from libs.adapters.spool.disk import DiskSpool
from libs.common.logging import configure_logging
from services.ingress.app import IngressService
from services.ingress.config import IngressSettings, load_ingress_settings
from services.ingress.rate_limiter import TokenBucketRateLimiter
from services.ingress.receiver import run_receiver


def build_service(settings: IngressSettings) -> IngressService:
    """Construct an :class:`IngressService` from *settings*."""
    bus = KafkaBusStub()

    spool = DiskSpool(settings.spool_dir) if settings.spool_enabled else None

    limiter = TokenBucketRateLimiter(
        rate=settings.rate_limit_per_sec,
        burst=settings.rate_limit_burst,
    )

    return IngressService(
        bus,
        spool=spool,
        rate_limiter=limiter,
        max_line_length=settings.max_line_length,
    )


def main() -> None:
    """Configure logging, build the service, and start the receiver."""
    configure_logging()
    settings = load_ingress_settings()
    service = build_service(settings)
    asyncio.run(
        run_receiver(
            service,
            host=settings.listen_host,
            udp_port=settings.listen_port_udp,
            tcp_port=settings.listen_port_tcp,
        ),
    )


if __name__ == "__main__":
    main()
