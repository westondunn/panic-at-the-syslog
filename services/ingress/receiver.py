"""Asyncio UDP + TCP syslog receiver for the ingress service."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from libs.common.errors import ValidationError
from libs.common.logging import get_logger

if TYPE_CHECKING:
    from services.ingress.app import IngressService

logger = get_logger("panic.services.ingress.receiver")


class SyslogUDPProtocol(asyncio.DatagramProtocol):
    """Asyncio datagram protocol that feeds syslog lines to *IngressService*."""

    def __init__(self, service: IngressService) -> None:
        self._service = service

    def datagram_received(self, data: bytes, addr: tuple[str, int]) -> None:
        try:
            line = data.decode("utf-8", errors="replace").strip("\r\n")
            self._service.receive_syslog_line(line, peer_address=addr[0])
        except ValidationError:
            logger.warning(
                "invalid syslog datagram",
                extra={"peer_address": addr[0]},
            )
        except Exception:
            logger.exception(
                "unexpected error handling UDP datagram",
                extra={"peer_address": addr[0]},
            )


class SyslogTCPHandler:
    """Callback handler for :func:`asyncio.start_server`."""

    def __init__(self, service: IngressService) -> None:
        self._service = service

    async def handle(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
    ) -> None:
        peer = writer.get_extra_info("peername")
        peer_address: str = peer[0] if peer else "unknown"
        try:
            while True:
                data = await reader.readline()
                if not data:
                    break
                line = data.decode("utf-8", errors="replace").strip("\r\n")
                try:
                    self._service.receive_syslog_line(
                        line, peer_address=peer_address,
                    )
                except ValidationError:
                    logger.warning(
                        "invalid syslog line on TCP connection",
                        extra={"peer_address": peer_address},
                    )
        except Exception:
            logger.exception(
                "unexpected error on TCP connection",
                extra={"peer_address": peer_address},
            )
        finally:
            writer.close()
            await writer.wait_closed()


async def run_receiver(
    service: IngressService,
    host: str,
    udp_port: int,
    tcp_port: int,
) -> None:
    """Start UDP and TCP syslog listeners and block until shutdown."""
    loop = asyncio.get_running_loop()

    udp_transport, _ = await loop.create_datagram_endpoint(
        lambda: SyslogUDPProtocol(service),
        local_addr=(host, udp_port),
    )

    tcp_handler = SyslogTCPHandler(service)
    tcp_server = await asyncio.start_server(
        tcp_handler.handle, host, tcp_port,
    )

    logger.info(
        "syslog UDP listener started on %s:%d", host, udp_port,
    )
    logger.info(
        "syslog TCP listener started on %s:%d", host, tcp_port,
    )

    try:
        await asyncio.Event().wait()
    finally:
        udp_transport.close()
        tcp_server.close()
        await tcp_server.wait_closed()
