from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class IngressSettings:
    listen_host: str = "0.0.0.0"
    listen_port_udp: int = 514
    listen_port_tcp: int = 514
    max_line_length: int = 8192
    rate_limit_per_sec: float = 5000.0
    rate_limit_burst: int = 10000
    spool_enabled: bool = False
    spool_dir: str = "/var/spool/panic-ingress"
    spool_ttl_seconds: int = 86400


def load_ingress_settings() -> IngressSettings:
    return IngressSettings(
        listen_host=os.getenv("INGRESS_LISTEN_HOST", "0.0.0.0"),
        listen_port_udp=int(os.getenv("INGRESS_LISTEN_PORT_UDP", "514")),
        listen_port_tcp=int(os.getenv("INGRESS_LISTEN_PORT_TCP", "514")),
        max_line_length=int(os.getenv("INGRESS_MAX_LINE_LENGTH", "8192")),
        rate_limit_per_sec=float(
            os.getenv("INGRESS_RATE_LIMIT_PER_SEC", "5000.0"),
        ),
        rate_limit_burst=int(os.getenv("INGRESS_RATE_LIMIT_BURST", "10000")),
        spool_enabled=os.getenv("INGRESS_SPOOL_ENABLED", "false").lower() in {"1", "true", "yes"},
        spool_dir=os.getenv(
            "INGRESS_SPOOL_DIR",
            "/var/spool/panic-ingress",
        ),
        spool_ttl_seconds=int(
            os.getenv("INGRESS_SPOOL_TTL_SECONDS", "86400"),
        ),
    )
