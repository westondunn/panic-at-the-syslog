from __future__ import annotations

import time


class TokenBucketRateLimiter:
    """Stdlib-only token-bucket rate limiter using ``time.monotonic``."""

    def __init__(self, rate: float, burst: int) -> None:
        self._rate = rate
        self._burst = burst
        self._tokens = float(burst)
        self._last: float = time.monotonic()

    def allow(self) -> bool:
        """Return *True* and consume a token if one is available."""
        now = time.monotonic()
        elapsed = now - self._last
        self._last = now

        self._tokens = min(
            float(self._burst),
            self._tokens + elapsed * self._rate,
        )

        if self._tokens >= 1.0:
            self._tokens -= 1.0
            return True
        return False
