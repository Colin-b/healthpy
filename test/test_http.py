import json
from responses import RequestsMock

import healthpy.http
from healthpy.testing import mock_http_health_datetime


def test_exception_health_check(mock_http_health_datetime):
    assert healthpy.http.check("test", "http://test/health") == (
        "fail",
        {
            "test:health": {
                "componentType": "http://test/health",
                "output": "Connection refused by Responses: GET http://test/health doesn't match Responses Mock",
                "status": "fail",
                "affectedEndpoints": None,
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    )


def test_exception_health_check_with_custom_status(
    monkeypatch, mock_http_health_datetime
):
    monkeypatch.setattr(healthpy, "fail_status", "custom failure")
    assert (
        "custom failure",
        {
            "test:health": {
                "componentType": "http://test/health",
                "output": "Connection refused by Responses: GET http://test/health doesn't match Responses Mock",
                "status": "custom failure",
                "affectedEndpoints": None,
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    ) == healthpy.http.check("test", "http://test/health")


def test_exception_health_check_as_warn(mock_http_health_datetime):
    assert (
        "warn",
        {
            "test:health": {
                "componentType": "http://test/health",
                "output": "Connection refused by Responses: GET http://test/health doesn't match Responses Mock",
                "status": "warn",
                "affectedEndpoints": None,
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    ) == healthpy.http.check("test", "http://test/health", failure_status="warn")


def test_exception_health_check_as_warn_even_with_custom_status(
    monkeypatch, mock_http_health_datetime
):
    monkeypatch.setattr(healthpy, "fail_status", "custom failure")
    monkeypatch.setattr(healthpy, "warn_status", "custom warning")
    assert (
        "warn provided",
        {
            "test:health": {
                "componentType": "http://test/health",
                "output": "Connection refused by Responses: GET http://test/health doesn't match Responses Mock",
                "status": "warn provided",
                "affectedEndpoints": None,
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    ) == healthpy.http.check(
        "test", "http://test/health", failure_status="warn provided"
    )


def test_error_health_check(mock_http_health_datetime, responses):
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
                "affectedEndpoints": None,
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    ) == healthpy.http.check("test", "http://test/health")


def test_error_health_check_as_warn(mock_http_health_datetime, responses):
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
                "affectedEndpoints": None,
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    ) == healthpy.http.check("test", "http://test/health", failure_status="warn")


def test_pass_status_health_check(mock_http_health_datetime, responses):
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
                "affectedEndpoints": None,
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    ) == healthpy.http.check("test", "http://test/health")


def test_pass_status_health_check_with_health_content_type(
    mock_http_health_datetime, responses
):
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
                "affectedEndpoints": None,
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    ) == healthpy.http.check("test", "http://test/health")


def test_pass_status_custom_health_check_pass(mock_http_health_datetime, responses):
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
                "affectedEndpoints": None,
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    ) == healthpy.http.check("test", "http://test/status", lambda resp: "pass")


def test_pass_status_custom_health_check_with_custom_pass_status(
    monkeypatch, mock_http_health_datetime, responses
):
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
                "affectedEndpoints": None,
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    ) == healthpy.http.check("test", "http://test/status", lambda resp: "pass")


def test_pass_status_custom_health_check_with_default_extractor(
    mock_http_health_datetime, responses
):
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
                "affectedEndpoints": None,
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    ) == healthpy.http.check("test", "http://test/status")


def test_pass_status_custom_health_check_with_default_extractor_and_custom_pass_status(
    monkeypatch, mock_http_health_datetime, responses
):
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
                "affectedEndpoints": None,
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    ) == healthpy.http.check("test", "http://test/status")


def test_warn_status_health_check(mock_http_health_datetime, responses):
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
                "affectedEndpoints": None,
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    ) == healthpy.http.check("test", "http://test/health")


def test_pass_status_custom_health_check_warn(mock_http_health_datetime, responses):
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
                "affectedEndpoints": None,
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    ) == healthpy.http.check("test", "http://test/status", lambda resp: "warn")


def test_fail_status_health_check(mock_http_health_datetime, responses):
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
                "affectedEndpoints": None,
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    ) == healthpy.http.check("test", "http://test/health")


def test_fail_status_custom_health_check(mock_http_health_datetime, responses):
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
                "affectedEndpoints": None,
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    ) == healthpy.http.check("test", "http://test/status", lambda resp: "fail")


def test_fail_status_when_server_is_down(mock_http_health_datetime):
    assert (
        "fail",
        {
            "test:health": {
                "componentType": "http://test/status",
                "output": "Connection refused by Responses: GET http://test/status doesn't match Responses Mock",
                "status": "fail",
                "affectedEndpoints": None,
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    ) == healthpy.http.check("test", "http://test/status")


def test_fail_status_when_server_is_down_as_warn(mock_http_health_datetime):
    assert (
        "warn",
        {
            "test:health": {
                "componentType": "http://test/status",
                "output": "Connection refused by Responses: GET http://test/status doesn't match Responses Mock",
                "status": "warn",
                "affectedEndpoints": None,
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    ) == healthpy.http.check("test", "http://test/status", failure_status="warn")


def test_show_affected_endpoints_when_endpoint_throws_exception(
    mock_http_health_datetime,
):
    assert (
        "warn",
        {
            "test:health": {
                "componentType": "http://test/status",
                "output": "Connection refused by Responses: GET http://test/status doesn't match Responses Mock",
                "status": "warn",
                "affectedEndpoints": ["/testroute/{userId}", "/status/{id}/idontexist"],
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    ) == healthpy.http.check(
        "test",
        "http://test/status",
        failure_status="warn",
        affected_endpoints=["/testroute/{userId}", "/status/{id}/idontexist"],
    )


def test_show_affected_endpoints_when_endpoint_throws_fail(
    mock_http_health_datetime, responses
):
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
                "affectedEndpoints": ["/testroute/{userId}", "/status/{id}/idontexist"],
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    ) == healthpy.http.check(
        "test",
        "http://test/status",
        lambda resp: "fail",
        affected_endpoints=["/testroute/{userId}", "/status/{id}/idontexist"],
    )


def test_show_affected_endpoints_when_request_failed_404(
    mock_http_health_datetime, responses
):
    responses.add(
        url="http://test/status", method=responses.GET, status=404, body="Not Found"
    )
    assert (
        "fail",
        {
            "test:health": {
                "componentType": "http://test/status",
                "status": "fail",
                "affectedEndpoints": ["/testroute/{userId}", "/status/{id}/idontexist"],
                "time": "2018-10-11T15:05:05.663979",
                "output": "Not Found",
            }
        },
    ) == healthpy.http.check(
        "test",
        "http://test/status",
        affected_endpoints=["/testroute/{userId}", "/status/{id}/idontexist"],
    )
