import pytest
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def patch_pg_pool(monkeypatch):
    # Stub out DB pool lifecycle so tests don't require a real Postgres
    async def _noop(*args, **kwargs):
        return None

    # Patch where it's used (main module)
    import main as app_main

    monkeypatch.setattr(app_main.PGSinglePool, "init_pool", _noop, raising=True)
    monkeypatch.setattr(app_main.PGSinglePool, "close_pool", _noop, raising=True)
    yield


def _client():
    from main import a_i

    return TestClient(a_i)


def test_root():
    with _client() as client:
        resp = client.get("/")
        assert resp.status_code == 200
        assert resp.json() == {"message": "Welcome to fast-skeleton"}


def test_health_v1():
    with _client() as client:
        resp = client.get("/api/v1/health")
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "ok"
        assert body["version"] == "v1"


def test_health_v2():
    with _client() as client:
        resp = client.get("/api/v2/health")
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "ok"
        assert body["version"] == "v2"


def test_user_v1():
    with _client() as client:
        resp = client.get("/api/v1/user")
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "ok"
        assert body["version"] == "v1"
        assert body["message"] == "User exist"


def test_user_v2():
    with _client() as client:
        resp = client.get("/api/v2/user")
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "ok"
        assert body["version"] == "v2"
        assert body["message"] == "User exist"


