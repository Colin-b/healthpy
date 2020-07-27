from typing import Any, List

import requests

from healthpy._http import _check, _is_json


class _Request:
    def __init__(self, url: str, **args):
        self.response = requests.get(url, timeout=args.pop("timeout", (1, 5)), **args)

    def is_error(self) -> bool:
        return not self.response.ok

    def content(self) -> Any:
        return (
            self.response.json()
            if _is_json(self.response.headers["content-type"])
            else self.response.text
        )


def check(
    service_name: str,
    url: str,
    status_extracting: callable = None,
    failure_status: str = None,
    affected_endpoints: List[str] = None,
    additional_keys: dict = None,
    error_status_extracting: callable = None,
    **requests_args,
) -> (str, dict):
    """
    Return Health "Checks object" for an external service connection.

    :param service_name: External service name.
    :param url: External service health check URL.
    :param status_extracting: Function returning status according to the JSON or text response (as parameter).
    Default to the way status should be extracted from a service following healthcheck RFC.
    :param error_status_extracting: Function returning status according to the JSON or text response (as parameter).
    Default to the way status should be extracted from a service following healthcheck RFC or fail_status.
    Note that the response might be None as this is called to extract the default status in case of failure as well.
    :param affected_endpoints: List of endpoints affected if dependency is down. Default to None.
    :param additional_keys: Additional user defined keys to send in checks.
    :return: A tuple with a string providing the status (amongst healthpy.*_status variable) and the "Checks object".
    Based on https://inadarei.github.io/rfc-healthcheck/
    """
    return _check(
        service_name=service_name,
        url=url,
        request_class=_Request,
        status_extracting=status_extracting,
        failure_status=failure_status,
        affected_endpoints=affected_endpoints,
        additional_keys=additional_keys,
        error_status_extracting=error_status_extracting,
        **requests_args,
    )
