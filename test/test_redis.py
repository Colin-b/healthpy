import unittest
import unittest.mock as mock

import redis

from healthpy.redis import check


class UTCDateTimeMock:
    @staticmethod
    def isoformat():
        return "2018-10-11T15:05:05.663979"


class RedisHealthTest(unittest.TestCase):
    @mock.patch.object(redis.Redis, "ping", return_value=1)
    @mock.patch.object(redis.Redis, "keys", return_value=["local"])
    @mock.patch("healthpy.redis.datetime")
    def test_redis_health_details_ok(self, datetime_mock, ping_mock, keys_mock):
        datetime_mock.utcnow = mock.Mock(return_value=UTCDateTimeMock)
        status, details = check("redis://test_url", "local_my_host")
        self.assertEqual(status, "pass")
        self.assertEqual(
            details,
            {
                "redis:ping": {
                    "componentType": "component",
                    "observedValue": "local_my_host can be found.",
                    "status": "pass",
                    "time": "2018-10-11T15:05:05.663979",
                }
            },
        )

    @mock.patch.object(redis.Redis, "ping")
    @mock.patch("healthpy.redis.datetime")
    def test_redis_health_details_cannot_connect_to_redis(
        self, datetime_mock, ping_mock
    ):
        datetime_mock.utcnow = mock.Mock(return_value=UTCDateTimeMock)
        ping_mock.side_effect = redis.exceptions.ConnectionError("Test message")

        status, details = check("redis://test_url", "")
        self.assertEqual(status, "fail")
        self.assertEqual(
            details,
            {
                "redis:ping": {
                    "componentType": "component",
                    "status": "fail",
                    "time": "2018-10-11T15:05:05.663979",
                    "output": "Test message",
                }
            },
        )

    @mock.patch.object(redis.Redis, "from_url")
    @mock.patch("healthpy.redis.datetime")
    def test_redis_health_details_cannot_retrieve_url(
        self, datetime_mock, from_url_mock
    ):
        datetime_mock.utcnow = mock.Mock(return_value=UTCDateTimeMock)
        from_url_mock.side_effect = redis.exceptions.ConnectionError("Test message")

        status, details = check("redis://test_url", "")
        self.assertEqual(status, "fail")
        self.assertEqual(
            details,
            {
                "redis:ping": {
                    "componentType": "component",
                    "status": "fail",
                    "time": "2018-10-11T15:05:05.663979",
                    "output": "Test message",
                }
            },
        )

    @mock.patch.object(redis.Redis, "ping", return_value=1)
    @mock.patch.object(redis.Redis, "keys", return_value=b"Those are bytes")
    @mock.patch("healthpy.redis.datetime")
    def test_redis_health_details_cannot_retrieve_keys_as_list(
        self, datetime_mock, ping_mock, keys_mock
    ):
        datetime_mock.utcnow = mock.Mock(return_value=UTCDateTimeMock)
        status, details = check("redis://test_url", "local_my_host")
        self.assertEqual(status, "fail")
        self.assertEqual(
            details,
            {
                "redis:ping": {
                    "componentType": "component",
                    "status": "fail",
                    "time": "2018-10-11T15:05:05.663979",
                    "output": "local_my_host cannot be found in b'Those " "are bytes'",
                }
            },
        )

    @mock.patch.object(redis.Redis, "ping", return_value=1)
    @mock.patch.object(redis.Redis, "keys", return_value=[b"local"])
    @mock.patch("healthpy.redis.datetime")
    def test_redis_health_details_retrieve_keys_as_bytes_list(
        self, datetime_mock, ping_mock, keys_mock
    ):
        datetime_mock.utcnow = mock.Mock(return_value=UTCDateTimeMock)
        status, details = check("redis://test_url", "local_my_host")
        self.assertEqual(status, "pass")
        self.assertEqual(
            details,
            {
                "redis:ping": {
                    "componentType": "component",
                    "status": "pass",
                    "time": "2018-10-11T15:05:05.663979",
                    "observedValue": "local_my_host can be found.",
                }
            },
        )

    @mock.patch.object(redis.Redis, "ping", return_value=1)
    @mock.patch.object(redis.Redis, "keys", return_value=[])
    @mock.patch("healthpy.redis.datetime")
    def test_redis_health_details_missing_key(
        self, datetime_mock, ping_mock, keys_mock
    ):
        datetime_mock.utcnow = mock.Mock(return_value=UTCDateTimeMock)
        status, details = check("redis://test_url", "local_my_host")
        self.assertEqual(status, "fail")
        self.assertEqual(
            details,
            {
                "redis:ping": {
                    "componentType": "component",
                    "status": "fail",
                    "time": "2018-10-11T15:05:05.663979",
                    "output": "local_my_host cannot be found in []",
                }
            },
        )
