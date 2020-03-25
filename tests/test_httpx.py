import json
import os

import pytest
from pytest_httpx import httpx_mock, HTTPXMock

import healthpy.httpx
from healthpy.testing import mock_http_health_datetime


def test_exception_health_check(mock_http_health_datetime, httpx_mock: HTTPXMock):
    assert healthpy.httpx.check("tests", "http://test/health") == (
        "fail",
        {
            "tests:health": {
                "componentType": "http://test/health",
                "output": "No mock can be found for GET request on http://test/health.",
                "status": "fail",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    )


def test_exception_health_check_additional_keys(
    mock_http_health_datetime, httpx_mock: HTTPXMock
):
    assert healthpy.httpx.check(
        "tests", "http://test/health", additional_keys={"custom": "test"}
    ) == (
        "fail",
        {
            "tests:health": {
                "componentType": "http://test/health",
                "output": "No mock can be found for GET request on http://test/health.",
                "status": "fail",
                "time": "2018-10-11T15:05:05.663979",
                "custom": "test",
            }
        },
    )


def test_exception_health_check_with_custom_status(
    monkeypatch, mock_http_health_datetime, httpx_mock: HTTPXMock
):
    monkeypatch.setattr(healthpy, "fail_status", "custom failure")
    assert healthpy.httpx.check("tests", "http://test/health") == (
        "custom failure",
        {
            "tests:health": {
                "componentType": "http://test/health",
                "output": "No mock can be found for GET request on http://test/health.",
                "status": "custom failure",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    )


def test_exception_health_check_as_warn(
    mock_http_health_datetime, httpx_mock: HTTPXMock
):
    assert healthpy.httpx.check(
        "tests", "http://test/health", failure_status="warn"
    ) == (
        "warn",
        {
            "tests:health": {
                "componentType": "http://test/health",
                "output": "No mock can be found for GET request on http://test/health.",
                "status": "warn",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    )


def test_exception_health_check_as_warn_even_with_custom_status(
    monkeypatch, mock_http_health_datetime, httpx_mock: HTTPXMock
):
    monkeypatch.setattr(healthpy, "fail_status", "custom failure")
    monkeypatch.setattr(healthpy, "warn_status", "custom warning")
    assert healthpy.httpx.check(
        "tests", "http://test/health", failure_status="warn provided"
    ) == (
        "warn provided",
        {
            "tests:health": {
                "componentType": "http://test/health",
                "output": "No mock can be found for GET request on http://test/health.",
                "status": "warn provided",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    )


def test_error_health_check(mock_http_health_datetime, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="http://test/health",
        method="GET",
        status_code=500,
        data='{"message": "An error occurred"}',
    )
    assert healthpy.httpx.check("tests", "http://test/health") == (
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
    mock_http_health_datetime, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(
        url="http://test/health",
        method="GET",
        status_code=500,
        json={"message": "An error occurred"},
        headers={"content-type": "application/json"},
    )
    assert healthpy.httpx.check(
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


def test_error_health_check_as_warn(mock_http_health_datetime, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="http://test/health",
        method="GET",
        status_code=500,
        json={"message": "An error occurred"},
        headers={"content-type": "application/json"},
    )
    assert healthpy.httpx.check(
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


def test_pass_status_health_check(mock_http_health_datetime, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="http://test/health",
        method="GET",
        status_code=200,
        json={
            "status": "pass",
            "version": "1",
            "releaseId": "1.2.3",
            "details": {"toto": "tata"},
        },
        headers={"content-type": "application/json"},
    )
    assert healthpy.httpx.check("tests", "http://test/health") == (
        "pass",
        {
            "tests:health": {
                "componentType": "http://test/health",
                "observedValue": {
                    "status": "pass",
                    "version": "1",
                    "releaseId": "1.2.3",
                    "details": {"toto": "tata"},
                },
                "status": "pass",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    )


def test_pass_status_health_check_additional_keys(
    mock_http_health_datetime, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(
        url="http://test/health",
        method="GET",
        status_code=200,
        json={
            "status": "pass",
            "version": "1",
            "releaseId": "1.2.3",
            "details": {"toto": "tata"},
        },
        headers={"content-type": "application/json"},
    )
    assert healthpy.httpx.check(
        "tests", "http://test/health", additional_keys={"custom": "test"}
    ) == (
        "pass",
        {
            "tests:health": {
                "componentType": "http://test/health",
                "observedValue": {
                    "status": "pass",
                    "version": "1",
                    "releaseId": "1.2.3",
                    "details": {"toto": "tata"},
                },
                "status": "pass",
                "time": "2018-10-11T15:05:05.663979",
                "custom": "test",
            }
        },
    )


def test_pass_status_health_check_with_health_content_type(
    mock_http_health_datetime, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(
        url="http://test/health",
        method="GET",
        status_code=200,
        data=json.dumps(
            {
                "status": "pass",
                "version": "1",
                "releaseId": "1.2.3",
                "details": {"toto": "tata"},
            }
        ),
        headers={"content-type": "application/health+json"},
    )
    assert healthpy.httpx.check("tests", "http://test/health") == (
        "pass",
        {
            "tests:health": {
                "componentType": "http://test/health",
                "observedValue": {
                    "status": "pass",
                    "version": "1",
                    "releaseId": "1.2.3",
                    "details": {"toto": "tata"},
                },
                "status": "pass",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    )


def test_pass_status_custom_health_check_pass(
    mock_http_health_datetime, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(
        url="http://test/status", method="GET", status_code=200, data="pong"
    )
    assert healthpy.httpx.check("tests", "http://test/status", lambda resp: "pass") == (
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
    monkeypatch, mock_http_health_datetime, httpx_mock: HTTPXMock
):
    monkeypatch.setattr(healthpy, "pass_status", "custom pass")
    httpx_mock.add_response(
        url="http://test/status", method="GET", status_code=200, data="pong"
    )
    assert healthpy.httpx.check("tests", "http://test/status", lambda resp: "pass") == (
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
    mock_http_health_datetime, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(
        url="http://test/status", method="GET", status_code=200, data="pong"
    )
    assert healthpy.httpx.check("tests", "http://test/status") == (
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
    monkeypatch, mock_http_health_datetime, httpx_mock: HTTPXMock
):
    monkeypatch.setattr(healthpy, "pass_status", "custom pass")
    httpx_mock.add_response(
        url="http://test/status", method="GET", status_code=200, data="pong"
    )
    assert healthpy.httpx.check("tests", "http://test/status") == (
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


def test_warn_status_health_check(mock_http_health_datetime, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="http://test/health",
        method="GET",
        status_code=200,
        json={
            "status": "warn",
            "version": "1",
            "releaseId": "1.2.3",
            "details": {"toto": "tata"},
        },
        headers={"content-type": "application/json"},
    )
    assert healthpy.httpx.check("tests", "http://test/health") == (
        "warn",
        {
            "tests:health": {
                "componentType": "http://test/health",
                "observedValue": {
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


def test_warn_status_http_error_health_check(
    mock_http_health_datetime, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(
        url="http://test/health",
        method="GET",
        status_code=429,
        json={
            "status": "warn",
            "version": "1",
            "releaseId": "1.2.3",
            "details": {"toto": "tata"},
        },
        headers={"content-type": "application/json"},
    )
    assert healthpy.httpx.check("tests", "http://test/health") == (
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
    mock_http_health_datetime, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(
        url="http://test/health", method="GET", status_code=500,
    )
    assert healthpy.httpx.check(
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
    mock_http_health_datetime, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(
        url="http://test/health",
        method="GET",
        status_code=400,
        json={
            "status": "fail",
            "version": "1",
            "releaseId": "1.2.3",
            "details": {"toto": "tata"},
        },
        headers={"content-type": "application/json"},
    )
    assert healthpy.httpx.check("tests", "http://test/health") == (
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


def test_warn_status_health_check_additional_keys(
    mock_http_health_datetime, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(
        url="http://test/health",
        method="GET",
        status_code=200,
        json={
            "status": "warn",
            "version": "1",
            "releaseId": "1.2.3",
            "details": {"toto": "tata"},
        },
        headers={"content-type": "application/json"},
    )
    assert healthpy.httpx.check(
        "tests", "http://test/health", additional_keys={"custom": "test"}
    ) == (
        "warn",
        {
            "tests:health": {
                "componentType": "http://test/health",
                "observedValue": {
                    "status": "warn",
                    "version": "1",
                    "releaseId": "1.2.3",
                    "details": {"toto": "tata"},
                },
                "status": "warn",
                "time": "2018-10-11T15:05:05.663979",
                "custom": "test",
            }
        },
    )


def test_pass_status_custom_health_check_warn(
    mock_http_health_datetime, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(
        url="http://test/status", method="GET", status_code=200, data="pong"
    )
    assert healthpy.httpx.check("tests", "http://test/status", lambda resp: "warn") == (
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


def test_fail_status_health_check(mock_http_health_datetime, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="http://test/health",
        method="GET",
        status_code=200,
        json={
            "status": "fail",
            "version": "1",
            "releaseId": "1.2.3",
            "details": {"toto": "tata"},
        },
        headers={"content-type": "application/json"},
    )
    assert healthpy.httpx.check("tests", "http://test/health") == (
        "fail",
        {
            "tests:health": {
                "componentType": "http://test/health",
                "observedValue": {
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


def test_fail_status_custom_health_check(
    mock_http_health_datetime, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(
        url="http://test/status", method="GET", status_code=200, data="pong"
    )
    assert healthpy.httpx.check("tests", "http://test/status", lambda resp: "fail") == (
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


def test_fail_status_when_server_is_down(
    mock_http_health_datetime, httpx_mock: HTTPXMock
):
    assert healthpy.httpx.check("tests", "http://test/status") == (
        "fail",
        {
            "tests:health": {
                "componentType": "http://test/status",
                "output": "No mock can be found for GET request on http://test/status.",
                "status": "fail",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    )


def test_fail_status_when_server_is_down_as_warn(
    mock_http_health_datetime, httpx_mock: HTTPXMock
):
    assert healthpy.httpx.check(
        "tests", "http://test/status", failure_status="warn"
    ) == (
        "warn",
        {
            "tests:health": {
                "componentType": "http://test/status",
                "output": "No mock can be found for GET request on http://test/status.",
                "status": "warn",
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    )


def test_show_affected_endpoints_when_endpoint_throws_exception(
    mock_http_health_datetime, httpx_mock: HTTPXMock
):
    assert healthpy.httpx.check(
        "tests",
        "http://test/status",
        failure_status="warn",
        affected_endpoints=["/testroute/{userId}", "/status/{id}/idontexist"],
    ) == (
        "warn",
        {
            "tests:health": {
                "componentType": "http://test/status",
                "output": "No mock can be found for GET request on http://test/status.",
                "status": "warn",
                "affectedEndpoints": ["/testroute/{userId}", "/status/{id}/idontexist"],
                "time": "2018-10-11T15:05:05.663979",
            }
        },
    )


def test_show_affected_endpoints_when_endpoint_throws_fail(
    mock_http_health_datetime, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(
        url="http://test/status", method="GET", status_code=200, data="pong"
    )
    assert healthpy.httpx.check(
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
    mock_http_health_datetime, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(
        url="http://test/status", method="GET", status_code=404, data="Not Found"
    )
    assert healthpy.httpx.check(
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
