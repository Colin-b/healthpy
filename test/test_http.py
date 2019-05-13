import unittest
import unittest.mock as mock
import json

import responses

from healthpy.http import check


class UTCDateTimeMock:
    @staticmethod
    def isoformat():
        return "2018-10-11T15:05:05.663979"


class HttpHealthTest(unittest.TestCase):
    @mock.patch("healthpy.http.datetime")
    @responses.activate
    def test_exception_health_check(self, datetime_mock):
        datetime_mock.utcnow = mock.Mock(return_value=UTCDateTimeMock)
        self.assertEqual(
            (
                "fail",
                {
                    "test:health": {
                        "componentType": "http://test/health",
                        "output": "Connection refused by Responses: GET http://test/health doesn't match Responses Mock",
                        "status": "fail",
                        "time": "2018-10-11T15:05:05.663979",
                    }
                },
            ),
            check("test", "http://test/health"),
        )

    @mock.patch("healthpy.http.datetime")
    @responses.activate
    def test_exception_health_check_as_warn(self, datetime_mock):
        datetime_mock.utcnow = mock.Mock(return_value=UTCDateTimeMock)
        self.assertEqual(
            (
                "warn",
                {
                    "test:health": {
                        "componentType": "http://test/health",
                        "output": "Connection refused by Responses: GET http://test/health doesn't match Responses Mock",
                        "status": "warn",
                        "time": "2018-10-11T15:05:05.663979",
                    }
                },
            ),
            check("test", "http://test/health", failure_status="warn"),
        )

    @mock.patch("healthpy.http.datetime")
    @responses.activate
    def test_error_health_check(self, datetime_mock):
        datetime_mock.utcnow = mock.Mock(return_value=UTCDateTimeMock)
        responses.add(
            url="http://test/health",
            method=responses.GET,
            status=500,
            json={"message": "An error occurred"},
        )
        self.assertEqual(
            (
                "fail",
                {
                    "test:health": {
                        "componentType": "http://test/health",
                        "output": '{"message": "An error occurred"}',
                        "status": "fail",
                        "time": "2018-10-11T15:05:05.663979",
                    }
                },
            ),
            check("test", "http://test/health"),
        )

    @mock.patch("healthpy.http.datetime")
    @responses.activate
    def test_error_health_check_as_warn(self, datetime_mock):
        datetime_mock.utcnow = mock.Mock(return_value=UTCDateTimeMock)
        responses.add(
            url="http://test/health",
            method=responses.GET,
            status=500,
            json={"message": "An error occurred"},
        )
        self.assertEqual(
            (
                "warn",
                {
                    "test:health": {
                        "componentType": "http://test/health",
                        "output": '{"message": "An error occurred"}',
                        "status": "warn",
                        "time": "2018-10-11T15:05:05.663979",
                    }
                },
            ),
            check("test", "http://test/health", failure_status="warn"),
        )

    @mock.patch("healthpy.http.datetime")
    @responses.activate
    def test_pass_status_health_check(self, datetime_mock):
        datetime_mock.utcnow = mock.Mock(return_value=UTCDateTimeMock)
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
        self.assertEqual(
            (
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
            ),
            check("test", "http://test/health"),
        )

    @mock.patch("healthpy.http.datetime")
    @responses.activate
    def test_pass_status_health_check_with_health_content_type(self, datetime_mock):
        datetime_mock.utcnow = mock.Mock(return_value=UTCDateTimeMock)
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
        self.assertEqual(
            (
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
            ),
            check("test", "http://test/health"),
        )

    @mock.patch("healthpy.http.datetime")
    @responses.activate
    def test_pass_status_custom_health_check(self, datetime_mock):
        datetime_mock.utcnow = mock.Mock(return_value=UTCDateTimeMock)
        responses.add(
            url="http://test/status", method=responses.GET, status=200, body="pong"
        )
        self.assertEqual(
            (
                "pass",
                {
                    "test:health": {
                        "componentType": "http://test/status",
                        "observedValue": "pong",
                        "status": "pass",
                        "time": "2018-10-11T15:05:05.663979",
                    }
                },
            ),
            check("test", "http://test/status", lambda resp: "pass"),
        )

    @mock.patch("healthpy.http.datetime")
    @responses.activate
    def test_pass_status_custom_health_check_with_default_extractor(
        self, datetime_mock
    ):
        datetime_mock.utcnow = mock.Mock(return_value=UTCDateTimeMock)
        responses.add(
            url="http://test/status", method=responses.GET, status=200, body="pong"
        )
        self.assertEqual(
            (
                "pass",
                {
                    "test:health": {
                        "componentType": "http://test/status",
                        "observedValue": "pong",
                        "status": "pass",
                        "time": "2018-10-11T15:05:05.663979",
                    }
                },
            ),
            check("test", "http://test/status"),
        )

    @mock.patch("healthpy.http.datetime")
    @responses.activate
    def test_warn_status_health_check(self, datetime_mock):
        datetime_mock.utcnow = mock.Mock(return_value=UTCDateTimeMock)
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
        self.assertEqual(
            (
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
            ),
            check("test", "http://test/health"),
        )

    @mock.patch("healthpy.http.datetime")
    @responses.activate
    def test_pass_status_custom_health_check(self, datetime_mock):
        datetime_mock.utcnow = mock.Mock(return_value=UTCDateTimeMock)
        responses.add(
            url="http://test/status", method=responses.GET, status=200, body="pong"
        )
        self.assertEqual(
            (
                "warn",
                {
                    "test:health": {
                        "componentType": "http://test/status",
                        "observedValue": "pong",
                        "status": "warn",
                        "time": "2018-10-11T15:05:05.663979",
                    }
                },
            ),
            check("test", "http://test/status", lambda resp: "warn"),
        )

    @mock.patch("healthpy.http.datetime")
    @responses.activate
    def test_fail_status_health_check(self, datetime_mock):
        datetime_mock.utcnow = mock.Mock(return_value=UTCDateTimeMock)
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
        self.assertEqual(
            (
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
            ),
            check("test", "http://test/health"),
        )

    @mock.patch("healthpy.http.datetime")
    @responses.activate
    def test_fail_status_custom_health_check(self, datetime_mock):
        datetime_mock.utcnow = mock.Mock(return_value=UTCDateTimeMock)
        responses.add(
            url="http://test/status", method=responses.GET, status=200, body="pong"
        )
        self.assertEqual(
            (
                "fail",
                {
                    "test:health": {
                        "componentType": "http://test/status",
                        "observedValue": "pong",
                        "status": "fail",
                        "time": "2018-10-11T15:05:05.663979",
                    }
                },
            ),
            check("test", "http://test/status", lambda resp: "fail"),
        )

    @mock.patch("healthpy.http.datetime")
    @responses.activate
    def test_fail_status_when_server_is_down(self, datetime_mock):
        datetime_mock.utcnow = mock.Mock(return_value=UTCDateTimeMock)
        self.assertEqual(
            (
                "fail",
                {
                    "test:health": {
                        "componentType": "http://test/status",
                        "output": "Connection refused by Responses: GET http://test/status doesn't match Responses Mock",
                        "status": "fail",
                        "time": "2018-10-11T15:05:05.663979",
                    }
                },
            ),
            check("test", "http://test/status"),
        )

    @mock.patch("healthpy.http.datetime")
    @responses.activate
    def test_fail_status_when_server_is_down_as_warn(self, datetime_mock):
        datetime_mock.utcnow = mock.Mock(return_value=UTCDateTimeMock)
        self.assertEqual(
            (
                "warn",
                {
                    "test:health": {
                        "componentType": "http://test/status",
                        "output": "Connection refused by Responses: GET http://test/status doesn't match Responses Mock",
                        "status": "warn",
                        "time": "2018-10-11T15:05:05.663979",
                    }
                },
            ),
            check("test", "http://test/status", failure_status="warn"),
        )
