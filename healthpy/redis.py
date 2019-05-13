from datetime import datetime

import redis


def check(url: str, key_pattern: str) -> (str, dict):
    """
    Return Health details for redis keys.

    :param url: Redis URL
    :param key_pattern: Pattern to look for in keys.
    :return: A tuple with a string providing the status (pass, warn, fail) and the details.
    Details are based on https://inadarei.github.io/rfc-healthcheck/
    """
    try:
        redis_server = redis.Redis.from_url(url)
        redis_server.ping()

        keys = redis_server.keys(key_pattern)

        if not keys or not isinstance(keys, list):
            return (
                "fail",
                {
                    "redis:ping": {
                        "componentType": "component",
                        "status": "fail",
                        "time": datetime.utcnow().isoformat(),
                        "output": f"{key_pattern} cannot be found in {keys}",
                    }
                },
            )

        return (
            "pass",
            {
                "redis:ping": {
                    "componentType": "component",
                    "observedValue": f"{key_pattern} can be found.",
                    "status": "pass",
                    "time": datetime.utcnow().isoformat(),
                }
            },
        )
    except Exception as e:
        return (
            "fail",
            {
                "redis:ping": {
                    "componentType": "component",
                    "status": "fail",
                    "time": datetime.utcnow().isoformat(),
                    "output": str(e),
                }
            },
        )
