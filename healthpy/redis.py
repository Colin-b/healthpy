from datetime import datetime

import redis

import healthpy


def check(url: str, key_pattern: str, additional_keys: dict = None) -> (str, dict):
    """
    Return Health "Checks object" for redis keys.

    :param url: Redis URL
    :param key_pattern: Pattern to look for in keys.
    :param additional_keys: Additional user defined keys to send in checks.
    :return: A tuple with a string providing the status (amongst healthpy.*_status variable) and the "Checks object".
    Based on https://inadarei.github.io/rfc-healthcheck/
    """
    additional_keys = additional_keys or {}
    try:
        redis_server = redis.Redis.from_url(url)
        redis_server.ping()

        keys = redis_server.keys(key_pattern)

        if not keys or not isinstance(keys, list):
            return (
                healthpy.fail_status,
                {
                    "redis:ping": {
                        "componentType": "component",
                        "status": healthpy.fail_status,
                        "time": datetime.utcnow().isoformat(),
                        "output": f"{key_pattern} cannot be found in {keys}",
                        **additional_keys,
                    }
                },
            )

        return (
            healthpy.pass_status,
            {
                "redis:ping": {
                    "componentType": "component",
                    "observedValue": f"{key_pattern} can be found.",
                    "status": healthpy.pass_status,
                    "time": datetime.utcnow().isoformat(),
                    **additional_keys,
                }
            },
        )
    except Exception as e:
        return (
            healthpy.fail_status,
            {
                "redis:ping": {
                    "componentType": "component",
                    "status": healthpy.fail_status,
                    "time": datetime.utcnow().isoformat(),
                    "output": str(e),
                    **additional_keys,
                }
            },
        )
