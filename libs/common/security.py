from __future__ import annotations

from typing import Any


SENSITIVE_KEYS = {"password", "token", "authorization", "secret", "api_key"}


def redact_payload(payload: dict[str, Any]) -> dict[str, Any]:
    redacted: dict[str, Any] = {}
    for key, value in payload.items():
        if key.lower() in SENSITIVE_KEYS:
            redacted[key] = "***REDACTED***"
        else:
            redacted[key] = value
    return redacted