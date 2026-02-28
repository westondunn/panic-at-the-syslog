"""Unit tests for services.ingress.rate_limiter.TokenBucketRateLimiter."""

from __future__ import annotations

import time

from services.ingress.rate_limiter import TokenBucketRateLimiter


# ---------------------------------------------------------------------------
# Burst behaviour
# ---------------------------------------------------------------------------


class TestBurstBehaviour:
    def test_allows_within_burst(self) -> None:
        rl = TokenBucketRateLimiter(rate=10.0, burst=5)

        results = [rl.allow() for _ in range(5)]

        assert all(results)

    def test_rejects_over_burst(self) -> None:
        # rate=0 prevents any refill between rapid calls
        rl = TokenBucketRateLimiter(rate=0.0, burst=3)

        for _ in range(3):
            assert rl.allow()
        assert not rl.allow()


# ---------------------------------------------------------------------------
# Token refill
# ---------------------------------------------------------------------------


class TestTokenRefill:
    def test_refills_over_time(self) -> None:
        # 100 tokens/sec → 0.1 s yields ~10 tokens; burst=1 caps at 1
        rl = TokenBucketRateLimiter(rate=100.0, burst=1)

        assert rl.allow()
        assert not rl.allow()

        time.sleep(0.1)

        assert rl.allow()
