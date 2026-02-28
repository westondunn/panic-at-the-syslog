from __future__ import annotations

import time

import jwt
import pytest
from httpx import ASGITransport, AsyncClient

from libs.adapters.auth import JwtAuthAdapter, JwtAuthStub
from libs.adapters.storage import InMemoryStorage
from services.api.app import ApiService, create_app

_TEST_SECRET = "test-only-not-a-real-secret"  # noqa: S105 — test-only value


@pytest.fixture()
def storage() -> InMemoryStorage:
    return InMemoryStorage()


@pytest.fixture()
def app(storage: InMemoryStorage) -> object:
    return create_app(auth=JwtAuthStub(), storage=storage)


@pytest.fixture()
def auth_header() -> dict[str, str]:
    return {"Authorization": "Bearer stub-token"}


# ---------------------------------------------------------------------------
# Health / readiness (no auth)
# ---------------------------------------------------------------------------


@pytest.mark.anyio
async def test_healthz_returns_ok(app: object) -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/healthz")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["service"] == "api"


@pytest.mark.anyio
async def test_readyz_returns_ready(app: object) -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/readyz")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ready"
    assert "checks" in body


# ---------------------------------------------------------------------------
# Auth enforcement
# ---------------------------------------------------------------------------


@pytest.mark.anyio
async def test_incidents_requires_auth(app: object) -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/v1/incidents")
    assert resp.status_code == 401


@pytest.mark.anyio
async def test_incidents_with_valid_token(
    app: object, storage: InMemoryStorage, auth_header: dict[str, str]
) -> None:
    storage.upsert("incidents", "inc-1", {"title": "Test incident"})
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/v1/incidents", headers=auth_header)
    assert resp.status_code == 200
    body = resp.json()
    assert len(body["items"]) == 1
    assert body["items"][0]["title"] == "Test incident"


# ---------------------------------------------------------------------------
# All read-model endpoints
# ---------------------------------------------------------------------------


@pytest.mark.anyio
@pytest.mark.parametrize(
    "path,collection",
    [
        ("/api/v1/findings", "findings"),
        ("/api/v1/insights", "insights"),
        ("/api/v1/devices", "devices"),
        ("/api/v1/review-queue", "review-queue"),
    ],
)
async def test_read_endpoints_return_items(
    app: object,
    storage: InMemoryStorage,
    auth_header: dict[str, str],
    path: str,
    collection: str,
) -> None:
    storage.upsert(collection, "item-1", {"id": "item-1"})
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get(path, headers=auth_header)
    assert resp.status_code == 200
    assert "items" in resp.json()
    assert len(resp.json()["items"]) == 1


# ---------------------------------------------------------------------------
# JwtAuthAdapter unit tests
# ---------------------------------------------------------------------------


def test_jwt_adapter_valid_token() -> None:
    adapter = JwtAuthAdapter(secret=_TEST_SECRET)
    token = jwt.encode(
        {"sub": "user-42", "roles": ["admin", "viewer"]},
        _TEST_SECRET,
        algorithm="HS256",
    )
    subject = adapter.validate_token(token)
    assert subject is not None
    assert subject.subject_id == "user-42"
    assert "admin" in subject.roles
    assert "viewer" in subject.roles


def test_jwt_adapter_expired_token() -> None:
    adapter = JwtAuthAdapter(secret=_TEST_SECRET)
    token = jwt.encode(
        {"sub": "user-1", "roles": ["viewer"], "exp": int(time.time()) - 60},
        _TEST_SECRET,
        algorithm="HS256",
    )
    assert adapter.validate_token(token) is None


def test_jwt_adapter_invalid_token() -> None:
    adapter = JwtAuthAdapter(secret=_TEST_SECRET)
    assert adapter.validate_token("not-a-jwt") is None


def test_jwt_adapter_missing_sub() -> None:
    adapter = JwtAuthAdapter(secret=_TEST_SECRET)
    token = jwt.encode({"roles": ["viewer"]}, _TEST_SECRET, algorithm="HS256")
    assert adapter.validate_token(token) is None


def test_jwt_adapter_empty_token() -> None:
    adapter = JwtAuthAdapter(secret=_TEST_SECRET)
    assert adapter.validate_token("") is None


# ---------------------------------------------------------------------------
# StorageAdapter.list
# ---------------------------------------------------------------------------


def test_storage_list_empty() -> None:
    storage = InMemoryStorage()
    assert storage.list("nonexistent") == []


def test_storage_list_with_items() -> None:
    storage = InMemoryStorage()
    storage.upsert("col", "a", {"val": 1})
    storage.upsert("col", "b", {"val": 2})
    items = storage.list("col")
    assert len(items) == 2
    vals = {item["val"] for item in items}
    assert vals == {1, 2}


# ---------------------------------------------------------------------------
# Backward compatibility
# ---------------------------------------------------------------------------


def test_api_service_health_backward_compat() -> None:
    svc = ApiService()
    health = svc.health()
    assert health["status"] == "ok"
    assert health["service"] == "api"
