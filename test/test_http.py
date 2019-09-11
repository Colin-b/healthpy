import json

import responses

import healthpy.http


class DateTimeMock:
    @staticmethod
    def utcnow():
        class UTCDateTimeMock:
            @staticmethod
            def isoformat():
                return "2018-10-11T15:05:05.663979"

        return UTCDateTimeMock


def test_exception_health_check(monkeypatch):
    monkeypatch.setattr(healthpy.http, "datetime", DateTimeMock)
    assert (
        "fail",
        {
            "test:health": {
                "componentType": "http://test/health",
                "output": "Connection refused by Responses: GET http://test/health doesn't match Responses Mock",
                "status": "fail",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    ) == healthpy.http.check("test", "http://test/health")


def test_exception_health_check_with_custom_status(monkeypatch):
    monkeypatch.setattr(healthpy.http, "datetime", DateTimeMock)
    monkeypatch.setattr(healthpy, "fail_status", "custom failure")
    assert (
        "custom failure",
        {
            "test:health": {
                "componentType": "http://test/health",
                "output": "Connection refused by Responses: GET http://test/health doesn't match Responses Mock",
                "status": "custom failure",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    ) == healthpy.http.check("test", "http://test/health")


def test_exception_health_check_as_warn(monkeypatch):
    monkeypatch.setattr(healthpy.http, "datetime", DateTimeMock)
    assert (
        "warn",
        {
            "test:health": {
                "componentType": "http://test/health",
                "output": "Connection refused by Responses: GET http://test/health doesn't match Responses Mock",
                "status": "warn",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    ) == healthpy.http.check("test", "http://test/health", failure_status="warn")


def test_exception_health_check_as_warn_even_with_custom_status(monkeypatch):
    monkeypatch.setattr(healthpy, "fail_status", "custom failure")
    monkeypatch.setattr(healthpy, "warn_status", "custom warning")
    monkeypatch.setattr(healthpy.http, "datetime", DateTimeMock)
    assert (
        "warn provided",
        {
            "test:health": {
                "componentType": "http://test/health",
                "output": "Connection refused by Responses: GET http://test/health doesn't match Responses Mock",
                "status": "warn provided",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    ) == healthpy.http.check(
        "test", "http://test/health", failure_status="warn provided"
    )


def test_error_health_check(monkeypatch):
    monkeypatch.setattr(healthpy.http, "datetime", DateTimeMock)
    responses.add(
        url="http://test/health",
        method=responses.GET,
        status=500,
        json={"message": "An error occurred"},
    )
    assert (
        "fail",
        {
            "test:health": {
                "componentType": "http://test/health",
                "output": '{"message": "An error occurred"}',
                "status": "fail",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    ) == healthpy.http.check("test", "http://test/health")


def test_error_health_check_as_warn(monkeypatch):
    monkeypatch.setattr(healthpy.http, "datetime", DateTimeMock)
    responses.add(
        url="http://test/health",
        method=responses.GET,
        status=500,
        json={"message": "An error occurred"},
    )
    assert (
        "warn",
        {
            "test:health": {
                "componentType": "http://test/health",
                "output": '{"message": "An error occurred"}',
                "status": "warn",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    ) == healthpy.http.check("test", "http://test/health", failure_status="warn")


def test_pass_status_health_check(monkeypatch):
    monkeypatch.setattr(healthpy.http, "datetime", DateTimeMock)
    responses.add(
        url="http://test/health",
        method=responses.GET,
        status=200,
        json={
            "status": "pass",
            "version": "1",
            "releaseId": "1.2.3",
            "details": {"toto": "tata"},
        },
    )
    assert (
        "pass",
        {
            "test:health": {
                "componentType": "http://test/health",
                "observedValue": {
                    "details": {"toto": "tata"},
                    "releaseId": "1.2.3",
                    "status": "pass",
                    "version": "1",
                },
                "status": "pass",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    ) == healthpy.http.check("test", "http://test/health")


def test_pass_status_health_check_with_health_content_type(monkeypatch):
    monkeypatch.setattr(healthpy.http, "datetime", DateTimeMock)
    responses.add(
        url="http://test/health",
        method=responses.GET,
        status=200,
        body=json.dumps(
            {
                "status": "pass",
                "version": "1",
                "releaseId": "1.2.3",
                "details": {"toto": "tata"},
            }
        ),
        content_type="application/health+json",
    )
    assert (
        "pass",
        {
            "test:health": {
                "componentType": "http://test/health",
                "observedValue": {
                    "details": {"toto": "tata"},
                    "releaseId": "1.2.3",
                    "status": "pass",
                    "version": "1",
                },
                "status": "pass",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    ) == healthpy.http.check("test", "http://test/health")


def test_pass_status_custom_health_check_pass(monkeypatch):
    monkeypatch.setattr(healthpy.http, "datetime", DateTimeMock)
    responses.add(
        url="http://test/status", method=responses.GET, status=200, body="pong"
    )
    assert (
        "pass",
        {
            "test:health": {
                "componentType": "http://test/status",
                "observedValue": "pong",
                "status": "pass",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    ) == healthpy.http.check("test", "http://test/status", lambda resp: "pass")


def test_pass_status_custom_health_check_with_custom_pass_status(monkeypatch):
    monkeypatch.setattr(healthpy.http, "datetime", DateTimeMock)
    monkeypatch.setattr(healthpy, "pass_status", "custom pass")
    responses.add(
        url="http://test/status", method=responses.GET, status=200, body="pong"
    )
    assert (
        "pass",
        {
            "test:health": {
                "componentType": "http://test/status",
                "observedValue": "pong",
                "status": "pass",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    ) == healthpy.http.check("test", "http://test/status", lambda resp: "pass")


def test_pass_status_custom_health_check_with_default_extractor(monkeypatch):
    monkeypatch.setattr(healthpy.http, "datetime", DateTimeMock)
    responses.add(
        url="http://test/status", method=responses.GET, status=200, body="pong"
    )
    assert (
        "pass",
        {
            "test:health": {
                "componentType": "http://test/status",
                "observedValue": "pong",
                "status": "pass",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    ) == healthpy.http.check("test", "http://test/status")


def test_pass_status_custom_health_check_with_default_extractor_and_custom_pass_status(
    monkeypatch,
):
    monkeypatch.setattr(healthpy.http, "datetime", DateTimeMock)
    monkeypatch.setattr(healthpy, "pass_status", "custom pass")
    responses.add(
        url="http://test/status", method=responses.GET, status=200, body="pong"
    )
    assert (
        "custom pass",
        {
            "test:health": {
                "componentType": "http://test/status",
                "observedValue": "pong",
                "status": "custom pass",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    ) == healthpy.http.check("test", "http://test/status")


def test_warn_status_health_check(monkeypatch):
    monkeypatch.setattr(healthpy.http, "datetime", DateTimeMock)
    responses.add(
        url="http://test/health",
        method=responses.GET,
        status=200,
        json={
            "status": "warn",
            "version": "1",
            "releaseId": "1.2.3",
            "details": {"toto": "tata"},
        },
    )
    assert (
        "warn",
        {
            "test:health": {
                "componentType": "http://test/health",
                "observedValue": {
                    "details": {"toto": "tata"},
                    "releaseId": "1.2.3",
                    "status": "warn",
                    "version": "1",
                },
                "status": "warn",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    ) == healthpy.http.check("test", "http://test/health")


def test_pass_status_custom_health_check_warn(monkeypatch):
    monkeypatch.setattr(healthpy.http, "datetime", DateTimeMock)
    responses.add(
        url="http://test/status", method=responses.GET, status=200, body="pong"
    )
    assert (
        "warn",
        {
            "test:health": {
                "componentType": "http://test/status",
                "observedValue": "pong",
                "status": "warn",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    ) == healthpy.http.check("test", "http://test/status", lambda resp: "warn")


def test_fail_status_health_check(monkeypatch):
    monkeypatch.setattr(healthpy.http, "datetime", DateTimeMock)
    responses.add(
        url="http://test/health",
        method=responses.GET,
        status=200,
        json={
            "status": "fail",
            "version": "1",
            "releaseId": "1.2.3",
            "details": {"toto": "tata"},
        },
    )
    assert (
        "fail",
        {
            "test:health": {
                "componentType": "http://test/health",
                "observedValue": {
                    "details": {"toto": "tata"},
                    "releaseId": "1.2.3",
                    "status": "fail",
                    "version": "1",
                },
                "status": "fail",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    ) == healthpy.http.check("test", "http://test/health")


def test_fail_status_custom_health_check(monkeypatch):
    monkeypatch.setattr(healthpy.http, "datetime", DateTimeMock)
    responses.add(
        url="http://test/status", method=responses.GET, status=200, body="pong"
    )
    assert (
        "fail",
        {
            "test:health": {
                "componentType": "http://test/status",
                "observedValue": "pong",
                "status": "fail",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    ) == healthpy.http.check("test", "http://test/status", lambda resp: "fail")


def test_fail_status_when_server_is_down(monkeypatch):
    monkeypatch.setattr(healthpy.http, "datetime", DateTimeMock)
    assert (
        "fail",
        {
            "test:health": {
                "componentType": "http://test/status",
                "output": "Connection refused by Responses: GET http://test/status doesn't match Responses Mock",
                "status": "fail",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    ) == healthpy.http.check("test", "http://test/status")


def test_fail_status_when_server_is_down_as_warn(monkeypatch):
    monkeypatch.setattr(healthpy.http, "datetime", DateTimeMock)
    assert (
        "warn",
        {
            "test:health": {
                "componentType": "http://test/status",
                "output": "Connection refused by Responses: GET http://test/status doesn't match Responses Mock",
                "status": "warn",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    ) == healthpy.http.check("test", "http://test/status", failure_status="warn")
