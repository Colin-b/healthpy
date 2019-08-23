import redis

import healthpy.redis


class DateTimeMock:
    @staticmethod
    def utcnow():
        class UTCDateTimeMock:
            @staticmethod
            def isoformat():
                return "2018-10-11T15:05:05.663979"

        return UTCDateTimeMock


def test_redis_health_details_ok(monkeypatch):
    monkeypatch.setattr(redis.Redis, "ping", lambda *args: 1)
    monkeypatch.setattr(redis.Redis, "keys", lambda *args: ["local"])
    monkeypatch.setattr(healthpy.redis, "datetime", DateTimeMock)

    status, details = healthpy.redis.check("redis://test_url", "local_my_host")
    assert status == "pass"
    assert details == {
        "redis:ping": {
            "componentType": "component",
            "observedValue": "local_my_host can be found.",
            "status": "pass",
            "time": "2018-10-11T15:05:05.663979",
        }
    }


def test_redis_health_details_cannot_connect_to_redis(monkeypatch):
    def fail_ping(*args):
        raise redis.exceptions.ConnectionError("Test message")

    monkeypatch.setattr(redis.Redis, "ping", fail_ping)
    monkeypatch.setattr(healthpy.redis, "datetime", DateTimeMock)

    status, details = healthpy.redis.check("redis://test_url", "")
    assert status == "fail"
    assert details == {
        "redis:ping": {
            "componentType": "component",
            "status": "fail",
            "time": "2018-10-11T15:05:05.663979",
            "output": "Test message",
        }
    }


def test_redis_health_details_cannot_retrieve_url(monkeypatch):
    def fail_from_url(*args):
        raise redis.exceptions.ConnectionError("Test message")

    monkeypatch.setattr(redis.Redis, "from_url", fail_from_url)
    monkeypatch.setattr(healthpy.redis, "datetime", DateTimeMock)

    status, details = healthpy.redis.check("redis://test_url", "")
    assert status == "fail"
    assert details == {
        "redis:ping": {
            "componentType": "component",
            "status": "fail",
            "time": "2018-10-11T15:05:05.663979",
            "output": "Test message",
        }
    }


def test_redis_health_details_cannot_retrieve_keys_as_list(monkeypatch):
    monkeypatch.setattr(redis.Redis, "ping", lambda *args: 1)
    monkeypatch.setattr(redis.Redis, "keys", lambda *args: b"Those are bytes")
    monkeypatch.setattr(healthpy.redis, "datetime", DateTimeMock)

    status, details = healthpy.redis.check("redis://test_url", "local_my_host")
    assert status == "fail"
    assert details == {
        "redis:ping": {
            "componentType": "component",
            "status": "fail",
            "time": "2018-10-11T15:05:05.663979",
            "output": "local_my_host cannot be found in b'Those " "are bytes'",
        }
    }


def test_redis_health_details_retrieve_keys_as_bytes_list(monkeypatch):
    monkeypatch.setattr(redis.Redis, "ping", lambda *args: 1)
    monkeypatch.setattr(redis.Redis, "keys", lambda *args: [b"local"])
    monkeypatch.setattr(healthpy.redis, "datetime", DateTimeMock)

    status, details = healthpy.redis.check("redis://test_url", "local_my_host")
    assert status == "pass"
    assert details == {
        "redis:ping": {
            "componentType": "component",
            "status": "pass",
            "time": "2018-10-11T15:05:05.663979",
            "observedValue": "local_my_host can be found.",
        }
    }


def test_redis_health_details_missing_key(monkeypatch):
    monkeypatch.setattr(redis.Redis, "ping", lambda *args: 1)
    monkeypatch.setattr(redis.Redis, "keys", lambda *args: [])
    monkeypatch.setattr(healthpy.redis, "datetime", DateTimeMock)

    status, details = healthpy.redis.check("redis://test_url", "local_my_host")
    assert status == "fail"
    assert details == {
        "redis:ping": {
            "componentType": "component",
            "status": "fail",
            "time": "2018-10-11T15:05:05.663979",
            "output": "local_my_host cannot be found in []",
        }
    }
