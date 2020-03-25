import json
from responses import RequestsMock

import healthpy.requests
from healthpy.testing import mock_http_health_datetime


def test_exception_health_check(mock_http_health_datetime):
    assert healthpy.requests.check("tests", "http://test/health") == (
        "fail",
        {
            "tests:health": {
                "componentType": "http://test/health",
                "output": "Connection refused by Responses - the call doesn't match any registered mock.\n\nRequest: \n- GET http://test/health\n\nAvailable matches:\n",
                "status": "fail",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    )


def test_exception_health_check_additional_keys(mock_http_health_datetime):
    assert healthpy.requests.check(
        "tests", "http://test/health", additional_keys={"custom": "test"}
    ) == (
        "fail",
        {
            "tests:health": {
                "componentType": "http://test/health",
                "output": "Connection refused by Responses - the call doesn't match any registered mock.\n\nRequest: \n- GET http://test/health\n\nAvailable matches:\n",
                "status": "fail",
                "time": "2018-10-11T15:05:05.663979",
                "custom": "test",
            }
        },
    )


def test_exception_health_check_with_custom_status(
    monkeypatch, mock_http_health_datetime
):
    monkeypatch.setattr(healthpy, "fail_status", "custom failure")
    assert healthpy.requests.check("tests", "http://test/health") == (
        "custom failure",
        {
            "tests:health": {
                "componentType": "http://test/health",
                "output": "Connection refused by Responses - the call doesn't match any registered mock.\n\nRequest: \n- GET http://test/health\n\nAvailable matches:\n",
                "status": "custom failure",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    )


def test_exception_health_check_as_warn(mock_http_health_datetime):
    assert healthpy.requests.check(
        "tests", "http://test/health", failure_status="warn"
    ) == (
        "warn",
        {
            "tests:health": {
                "componentType": "http://test/health",
                "output": "Connection refused by Responses - the call doesn't match any registered mock.\n\nRequest: \n- GET http://test/health\n\nAvailable matches:\n",
                "status": "warn",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    )


def test_exception_health_check_as_warn_even_with_custom_status(
    monkeypatch, mock_http_health_datetime
):
    monkeypatch.setattr(healthpy, "fail_status", "custom failure")
    monkeypatch.setattr(healthpy, "warn_status", "custom warning")
    assert healthpy.requests.check(
        "tests", "http://test/health", failure_status="warn provided"
    ) == (
        "warn provided",
        {
            "tests:health": {
                "componentType": "http://test/health",
                "output": "Connection refused by Responses - the call doesn't match any registered mock.\n\nRequest: \n- GET http://test/health\n\nAvailable matches:\n",
                "status": "warn provided",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    )


def test_error_health_check(mock_http_health_datetime, responses: RequestsMock):
    responses.add(
        url="http://test/health",
        method=responses.GET,
        status=500,
        body='{"message": "An error occurred"}',
    )
    assert healthpy.requests.check("tests", "http://test/health") == (
        "fail",
        {
            "tests:health": {
                "componentType": "http://test/health",
                "output": '{"message": "An error occurred"}',
                "status": "fail",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    )


def test_error_health_check_additional_keys(
    mock_http_health_datetime, responses: RequestsMock
):
    responses.add(
        url="http://test/health",
        method=responses.GET,
        status=500,
        json={"message": "An error occurred"},
    )
    assert healthpy.requests.check(
        "tests", "http://test/health", additional_keys={"custom": "test"}
    ) == (
        "fail",
        {
            "tests:health": {
                "componentType": "http://test/health",
                "output": {"message": "An error occurred"},
                "status": "fail",
                "time": "2018-10-11T15:05:05.663979",
                "custom": "test",
            }
        },
    )


def test_error_health_check_as_warn(mock_http_health_datetime, responses: RequestsMock):
    responses.add(
        url="http://test/health",
        method=responses.GET,
        status=500,
        json={"message": "An error occurred"},
    )
    assert healthpy.requests.check(
        "tests", "http://test/health", failure_status="warn"
    ) == (
        "warn",
        {
            "tests:health": {
                "componentType": "http://test/health",
                "output": {"message": "An error occurred"},
                "status": "warn",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    )


def test_pass_status_health_check(mock_http_health_datetime, responses: RequestsMock):
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
    assert healthpy.requests.check("tests", "http://test/health") == (
        "pass",
        {
            "tests:health": {
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
    )


def test_pass_status_health_check_additional_keys(
    mock_http_health_datetime, responses: RequestsMock
):
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
    assert healthpy.requests.check(
        "tests", "http://test/health", additional_keys={"custom": "test"}
    ) == (
        "pass",
        {
            "tests:health": {
                "componentType": "http://test/health",
                "observedValue": {
                    "details": {"toto": "tata"},
                    "releaseId": "1.2.3",
                    "status": "pass",
                    "version": "1",
                },
                "status": "pass",
                "time": "2018-10-11T15:05:05.663979",
                "custom": "test",
            }
        },
    )


def test_pass_status_health_check_with_health_content_type(
    mock_http_health_datetime, responses: RequestsMock
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
    assert healthpy.requests.check("tests", "http://test/health") == (
        "pass",
        {
            "tests:health": {
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
    )


def test_pass_status_custom_health_check_pass(
    mock_http_health_datetime, responses: RequestsMock
):
    responses.add(
        url="http://test/status", method=responses.GET, status=200, body="pong"
    )
    assert healthpy.requests.check(
        "tests", "http://test/status", lambda resp: "pass"
    ) == (
        "pass",
        {
            "tests:health": {
                "componentType": "http://test/status",
                "observedValue": "pong",
                "status": "pass",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    )


def test_pass_status_custom_health_check_with_custom_pass_status(
    monkeypatch, mock_http_health_datetime, responses: RequestsMock
):
    monkeypatch.setattr(healthpy, "pass_status", "custom pass")
    responses.add(
        url="http://test/status", method=responses.GET, status=200, body="pong"
    )
    assert healthpy.requests.check(
        "tests", "http://test/status", lambda resp: "pass"
    ) == (
        "pass",
        {
            "tests:health": {
                "componentType": "http://test/status",
                "observedValue": "pong",
                "status": "pass",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    )


def test_pass_status_custom_health_check_with_default_extractor(
    mock_http_health_datetime, responses: RequestsMock
):
    responses.add(
        url="http://test/status", method=responses.GET, status=200, body="pong"
    )
    assert healthpy.requests.check("tests", "http://test/status") == (
        "pass",
        {
            "tests:health": {
                "componentType": "http://test/status",
                "observedValue": "pong",
                "status": "pass",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    )


def test_pass_status_custom_health_check_with_default_extractor_and_custom_pass_status(
    monkeypatch, mock_http_health_datetime, responses: RequestsMock
):
    monkeypatch.setattr(healthpy, "pass_status", "custom pass")
    responses.add(
        url="http://test/status", method=responses.GET, status=200, body="pong"
    )
    assert healthpy.requests.check("tests", "http://test/status") == (
        "custom pass",
        {
            "tests:health": {
                "componentType": "http://test/status",
                "observedValue": "pong",
                "status": "custom pass",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    )


def test_warn_status_http_error_health_check(
    mock_http_health_datetime, responses: RequestsMock
):
    responses.add(
        url="http://test/health",
        method=responses.GET,
        status=429,
        json={
            "status": "warn",
            "version": "1",
            "releaseId": "1.2.3",
            "details": {"toto": "tata"},
        },
    )
    assert healthpy.requests.check("tests", "http://test/health") == (
        "warn",
        {
            "tests:health": {
                "componentType": "http://test/health",
                "output": {
                    "status": "warn",
                    "version": "1",
                    "releaseId": "1.2.3",
                    "details": {"toto": "tata"},
                },
                "status": "warn",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    )


def test_custom_http_error_status_health_check(
    mock_http_health_datetime, responses: RequestsMock
):
    responses.add(
        url="http://test/health", method=responses.GET, status=500,
    )
    assert healthpy.requests.check(
        "tests",
        "http://test/health",
        error_status_extracting=lambda x: healthpy.warn_status,
    ) == (
        "warn",
        {
            "tests:health": {
                "componentType": "http://test/health",
                "output": "",
                "status": "warn",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    )


def test_fail_status_http_error_health_check(
    mock_http_health_datetime, responses: RequestsMock
):
    responses.add(
        url="http://test/health",
        method=responses.GET,
        status=400,
        json={
            "status": "fail",
            "version": "1",
            "releaseId": "1.2.3",
            "details": {"toto": "tata"},
        },
    )
    assert healthpy.requests.check("tests", "http://test/health") == (
        "fail",
        {
            "tests:health": {
                "componentType": "http://test/health",
                "output": {
                    "status": "fail",
                    "version": "1",
                    "releaseId": "1.2.3",
                    "details": {"toto": "tata"},
                },
                "status": "fail",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    )


def test_warn_status_health_check(mock_http_health_datetime, responses: RequestsMock):
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
    assert healthpy.requests.check("tests", "http://test/health") == (
        "warn",
        {
            "tests:health": {
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
    )


def test_warn_status_health_check_additional_keys(
    mock_http_health_datetime, responses: RequestsMock
):
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
    assert healthpy.requests.check(
        "tests", "http://test/health", additional_keys={"custom": "test"}
    ) == (
        "warn",
        {
            "tests:health": {
                "componentType": "http://test/health",
                "observedValue": {
                    "details": {"toto": "tata"},
                    "releaseId": "1.2.3",
                    "status": "warn",
                    "version": "1",
                },
                "status": "warn",
                "time": "2018-10-11T15:05:05.663979",
                "custom": "test",
            }
        },
    )


def test_pass_status_custom_health_check_warn(
    mock_http_health_datetime, responses: RequestsMock
):
    responses.add(
        url="http://test/status", method=responses.GET, status=200, body="pong"
    )
    assert healthpy.requests.check(
        "tests", "http://test/status", lambda resp: "warn"
    ) == (
        "warn",
        {
            "tests:health": {
                "componentType": "http://test/status",
                "observedValue": "pong",
                "status": "warn",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    )


def test_fail_status_health_check(mock_http_health_datetime, responses: RequestsMock):
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
    assert healthpy.requests.check("tests", "http://test/health") == (
        "fail",
        {
            "tests:health": {
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
    )


def test_fail_status_custom_health_check(
    mock_http_health_datetime, responses: RequestsMock
):
    responses.add(
        url="http://test/status", method=responses.GET, status=200, body="pong"
    )
    assert healthpy.requests.check(
        "tests", "http://test/status", lambda resp: "fail"
    ) == (
        "fail",
        {
            "tests:health": {
                "componentType": "http://test/status",
                "observedValue": "pong",
                "status": "fail",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    )


def test_fail_status_when_server_is_down(mock_http_health_datetime):
    assert healthpy.requests.check("tests", "http://test/status") == (
        "fail",
        {
            "tests:health": {
                "componentType": "http://test/status",
                "output": "Connection refused by Responses - the call doesn't match any registered mock.\n\nRequest: \n- GET http://test/status\n\nAvailable matches:\n",
                "status": "fail",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    )


def test_fail_status_when_server_is_down_as_warn(mock_http_health_datetime):
    assert healthpy.requests.check(
        "tests", "http://test/status", failure_status="warn"
    ) == (
        "warn",
        {
            "tests:health": {
                "componentType": "http://test/status",
                "output": "Connection refused by Responses - the call doesn't match any registered mock.\n\nRequest: \n- GET http://test/status\n\nAvailable matches:\n",
                "status": "warn",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    )


def test_show_affected_endpoints_when_endpoint_throws_exception(
    mock_http_health_datetime,
):
    assert healthpy.requests.check(
        "tests",
        "http://test/status",
        failure_status="warn",
        affected_endpoints=["/testroute/{userId}", "/status/{id}/idontexist"],
    ) == (
        "warn",
        {
            "tests:health": {
                "componentType": "http://test/status",
                "output": "Connection refused by Responses - the call doesn't match any registered mock.\n\nRequest: \n- GET http://test/status\n\nAvailable matches:\n",
                "status": "warn",
                "affectedEndpoints": ["/testroute/{userId}", "/status/{id}/idontexist"],
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    )


def test_show_affected_endpoints_when_endpoint_throws_fail(
    mock_http_health_datetime, responses: RequestsMock
):
    responses.add(
        url="http://test/status", method=responses.GET, status=200, body="pong"
    )
    assert healthpy.requests.check(
        "tests",
        "http://test/status",
        lambda resp: "fail",
        affected_endpoints=["/testroute/{userId}", "/status/{id}/idontexist"],
    ) == (
        "fail",
        {
            "tests:health": {
                "componentType": "http://test/status",
                "observedValue": "pong",
                "status": "fail",
                "affectedEndpoints": ["/testroute/{userId}", "/status/{id}/idontexist"],
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    )


def test_show_affected_endpoints_when_request_failed_404(
    mock_http_health_datetime, responses: RequestsMock
):
    responses.add(
        url="http://test/status", method=responses.GET, status=404, body="Not Found"
    )
    assert healthpy.requests.check(
        "tests",
        "http://test/status",
        affected_endpoints=["/testroute/{userId}", "/status/{id}/idontexist"],
    ) == (
        "fail",
        {
            "tests:health": {
                "componentType": "http://test/status",
                "status": "fail",
                "affectedEndpoints": ["/testroute/{userId}", "/status/{id}/idontexist"],
                "time": "2018-10-11T15:05:05.663979",
                "output": "Not Found",
            }
        },
    )
