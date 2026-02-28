from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import jwt

from libs.common.logging import get_logger

logger = get_logger("panic.adapters.auth")


@dataclass(frozen=True)
class AuthSubject:
    subject_id: str
    roles: tuple[str, ...]


class AuthAdapter(Protocol):
    def validate_token(self, token: str) -> AuthSubject | None: ...


class JwtAuthAdapter:
    """Production JWT adapter using HS256 symmetric signing."""

    def __init__(self, secret: str, algorithms: list[str] | None = None) -> None:
        self._secret = secret
        self._algorithms = algorithms or ["HS256"]

    def validate_token(self, token: str) -> AuthSubject | None:
        if not token:
            return None
        try:
            payload = jwt.decode(token, self._secret, algorithms=self._algorithms)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None
        sub = payload.get("sub")
        if not sub:
            return None
        roles = payload.get("roles", [])
        if isinstance(roles, str):
            roles = [roles]
        return AuthSubject(subject_id=sub, roles=tuple(roles))


class JwtAuthStub:
    """Tier 1 default auth placeholder."""

    def validate_token(self, token: str) -> AuthSubject | None:
        if not token:
            return None
        return AuthSubject(subject_id="local-user", roles=("viewer",))