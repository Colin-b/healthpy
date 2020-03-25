from typing import Any, List

import httpx

from healthpy._http import _check, _is_json


class _Request:
    def __init__(self, url: str, **args):
        with httpx.Client() as client:
            self.response = client.get(url, timeout=args.pop("timeout", (1, 5)), **args)

    def is_error(self) -> bool:
        return self.response.is_error

    def content(self) -> Any:
        return (
            self.response.json()
            if _is_json(self.response.headers.get("content-type"))
            else self.response.text
        )


def check(
    service_name: str,
    url: str,
    status_extracting: callable = None,
    failure_status: str = None,
    affected_endpoints: List[str] = None,
    additional_keys: dict = None,
    **httpx_args,
) -> (str, dict):
    """
    Return Health "Checks object" for an external service connection.

    :param service_name: External service name.
    :param url: External service health check URL.
    :param status_extracting: Function returning status according to the JSON or text response (as parameter).
    Default to the way status should be extracted from a service following healthcheck RFC.
    :param failure_status: Status to return in case of failure (Exception or HTTP rejection). healthpy.fail_status by default.
    :param affected_endpoints: List of endpoints affected if dependency is down. Default to None.
    :param additional_keys: Additional user defined keys to send in checks.
    :return: A tuple with a string providing the status (amongst healthpy.*_status variable) and the "Checks object".
    Based on https://inadarei.github.io/rfc-healthcheck/
    """
    return _check(
        service_name,
        url,
        _Request,
        status_extracting,
        failure_status,
        affected_endpoints,
        additional_keys,
        **httpx_args,
    )