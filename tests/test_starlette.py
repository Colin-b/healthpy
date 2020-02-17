from starlette.applications import Starlette
from starlette.testclient import TestClient

from healthpy.starlette import add_consul_health_endpoint


def test_consul_health_endpoint_pass():
    async def health_check():
        return "pass", {}

    app = Starlette()
    add_consul_health_endpoint(app, health_check, release_id="1.2.3")
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {
            "checks": {},
            "releaseId": "1.2.3",
            "status": "pass",
            "version": "1",
        }


def test_consul_health_endpoint_warn():
    async def health_check():
        return "warn", {}

    app = Starlette()
    add_consul_health_endpoint(app, health_check, release_id="1.2.3")
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 429
        assert response.json() == {
            "checks": {},
            "releaseId": "1.2.3",
            "status": "warn",
            "version": "1",
        }


def test_consul_health_endpoint_fail():
    async def health_check():
        return "fail", {}

    app = Starlette()
    add_consul_health_endpoint(app, health_check, release_id="1.2.3")
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 400
        assert response.json() == {
            "checks": {},
            "releaseId": "1.2.3",
            "status": "fail",
            "version": "1",
        }


def test_consul_health_endpoint_failure():
    async def failing():
        raise Exception("failure explanation")

    app = Starlette()
    add_consul_health_endpoint(app, failing, release_id="1.2.3")
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 400
        assert response.json() == {
            "output": "failure explanation",
            "releaseId": "1.2.3",
            "status": "fail",
            "version": "1",
        }
