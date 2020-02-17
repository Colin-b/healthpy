from starlette.applications import Starlette
from starlette.testclient import TestClient

from healthpy.starlette import add_consul_health_endpoint


def test_consul_health_endpoint_pass():
    app = Starlette()
    add_consul_health_endpoint(app, lambda: ("pass", {}), release_id="1.2.3")
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
    app = Starlette()
    add_consul_health_endpoint(app, lambda: ("warn", {}), release_id="1.2.3")
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
    app = Starlette()
    add_consul_health_endpoint(app, lambda: ("fail", {}), release_id="1.2.3")
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
    def failing():
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
