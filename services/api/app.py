from __future__ import annotations

import os
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from libs.adapters.auth import AuthSubject, JwtAuthAdapter, JwtAuthStub
from libs.adapters.storage import InMemoryStorage
from libs.common.logging import get_logger

logger = get_logger("panic.services.api")

_bearer_scheme = HTTPBearer(auto_error=False)


class ApiService:
    def __init__(
        self,
        *,
        auth: Any | None = None,
        storage: Any | None = None,
    ) -> None:
        self.auth = auth or JwtAuthStub()
        self.storage = storage or InMemoryStorage()

    def health(self) -> dict[str, str]:
        return {"status": "ok", "service": "api"}

    def readiness(self) -> dict[str, Any]:
        return {"status": "ready", "checks": {"storage": "ok"}}

    def list_collection(self, collection: str) -> dict[str, list[dict[str, Any]]]:
        items = self.storage.list(collection)
        return {"items": items}


def _build_auth_dependency(service: ApiService):
    async def require_auth(
        request: Request,
        credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
    ) -> AuthSubject:
        if credentials is None:
            raise HTTPException(status_code=401, detail="Missing authentication token")
        subject = service.auth.validate_token(credentials.credentials)
        if subject is None:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        correlation_id = request.headers.get("x-correlation-id", "")
        logger.info(
            "authenticated request",
            extra={
                "correlation_id": correlation_id,
                "subject_id": subject.subject_id,
                "roles": subject.roles,
            },
        )
        return subject

    return require_auth


def create_app(
    *,
    auth: Any | None = None,
    storage: Any | None = None,
) -> FastAPI:
    if auth is None:
        secret = os.getenv("PANIC_JWT_SECRET", "")
        auth = JwtAuthAdapter(secret=secret) if secret else JwtAuthStub()

    service = ApiService(auth=auth, storage=storage)
    require_auth = _build_auth_dependency(service)

    app = FastAPI(title="Panic! At The Syslog API", version="0.1.0")

    @app.get("/healthz")
    async def healthz() -> dict[str, str]:
        return service.health()

    @app.get("/readyz")
    async def readyz() -> dict[str, Any]:
        return service.readiness()

    @app.get("/api/v1/incidents")
    async def list_incidents(
        _subject: AuthSubject = Depends(require_auth),
    ) -> dict[str, list[dict[str, Any]]]:
        return service.list_collection("incidents")

    @app.get("/api/v1/findings")
    async def list_findings(
        _subject: AuthSubject = Depends(require_auth),
    ) -> dict[str, list[dict[str, Any]]]:
        return service.list_collection("findings")

    @app.get("/api/v1/insights")
    async def list_insights(
        _subject: AuthSubject = Depends(require_auth),
    ) -> dict[str, list[dict[str, Any]]]:
        return service.list_collection("insights")

    @app.get("/api/v1/devices")
    async def list_devices(
        _subject: AuthSubject = Depends(require_auth),
    ) -> dict[str, list[dict[str, Any]]]:
        return service.list_collection("devices")

    @app.get("/api/v1/review-queue")
    async def list_review_queue(
        _subject: AuthSubject = Depends(require_auth),
    ) -> dict[str, list[dict[str, Any]]]:
        return service.list_collection("review-queue")

    return app