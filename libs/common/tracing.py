from __future__ import annotations

from contextlib import contextmanager
from time import perf_counter
from typing import Iterator

from libs.common.logging import get_logger


@contextmanager
def trace_span(span_name: str) -> Iterator[None]:
    logger = get_logger("panic.tracing")
    started = perf_counter()
    logger.debug("span.start name=%s", span_name)
    try:
        yield
    finally:
        elapsed_ms = (perf_counter() - started) * 1000
        logger.debug("span.end name=%s elapsed_ms=%.2f", span_name, elapsed_ms)