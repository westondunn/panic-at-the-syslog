from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class AuthSubject:
    subject_id: str
    roles: tuple[str, ...]


class AuthAdapter(Protocol):
    def validate_token(self, token: str) -> AuthSubject | None: ...


class JwtAuthStub:
    """Tier 1 default auth placeholder."""

    def validate_token(self, token: str) -> AuthSubject | None:
        if not token:
            return None
        return AuthSubject(subject_id="local-user", roles=("viewer",))