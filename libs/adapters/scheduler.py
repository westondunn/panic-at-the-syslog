from __future__ import annotations

from datetime import datetime, timezone
from typing import Callable, Protocol


class SchedulerAdapter(Protocol):
    def schedule(self, job_name: str, callback: Callable[[], None]) -> None: ...


class InlineScheduler:
    def schedule(self, job_name: str, callback: Callable[[], None]) -> None:
        _ = (job_name, datetime.now(timezone.utc))
        callback()