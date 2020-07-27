import datetime
import re
from typing import List, Any, Optional
import warnings

import healthpy


def _is_json(content_type: Optional[str]) -> bool:
    return re.match(r"application/(health\+)?json", content_type or "") is not None


def _api_health_status(health_response: Any) -> str:
    if isinstance(health_response, dict):
        return health_response.get("status", healthpy.pass_status)
    return healthpy.pass_status


def _api_error_health_status(health_response: Any) -> str:
    if isinstance(health_response, dict):
        return health_response.get("status", healthpy.fail_status)
    return healthpy.fail_status


def safe_error_status_extracting(error_status_extracting: callable) -> str:
    try:
        return error_status_extracting(None)
    except:
        return healthpy.fail_status


def _check(
    service_name: str,
    url: str,
    request_class,
    status_extracting: callable = None,
    failure_status: str = None,
    affected_endpoints: List[str] = None,
    additional_keys: dict = None,
    error_status_extracting: callable = None,
    **kwargs,
) -> (str, dict):
    """
    Return Health "Checks object" for an external service connection.

    :param service_name: External service name.
    :param url: External service health check URL.
    :param status_extracting: Function returning status according to the JSON or text response (as parameter).
    Default to the way status should be extracted from a service following healthcheck RFC or pass_status.
    :param error_status_extracting: Function returning status according to the JSON or text response (as parameter).
    Default to the way status should be extracted from a service following healthcheck RFC or fail_status.
    Note that the response might be None as this is called to extract the default status in case of failure as well.
    :param affected_endpoints: List of endpoints affected if dependency is down. Default to None.
    :param additional_keys: Additional user defined keys to send in checks.
    :return: A tuple with a string providing the status (amongst healthpy.*_status variable) and the "Checks object".
    Based on https://inadarei.github.io/rfc-healthcheck/
    """
    try:
        request = request_class(url, **kwargs)
        response = request.content()
        if request.is_error():
            if not error_status_extracting:
                error_status_extracting = _api_error_health_status

            if failure_status:
                warnings.warn(
                    "failure_status is deprecated and should not be used anymore. Use error_status_extracting instead.",
                    DeprecationWarning,
                )

            status = failure_status or error_status_extracting(response)
            check = {"output": response} if status != healthpy.pass_status else {}
        else:
            if not status_extracting:
                status_extracting = _api_health_status

            status = status_extracting(response)
            check = {"observedValue": response}
    except Exception as e:
        if failure_status:
            warnings.warn(
                "failure_status is deprecated and should not be used anymore. Use error_status_extracting instead.",
                DeprecationWarning,
            )
        status = failure_status or safe_error_status_extracting(error_status_extracting)
        check = {"output": str(e)} if status != healthpy.pass_status else {}

    if affected_endpoints and status != healthpy.pass_status:
        check["affectedEndpoints"] = affected_endpoints

    if additional_keys:
        check.update(additional_keys)

    return (
        status,
        {
            f"{service_name}:health": {
                "componentType": url,
                "status": status,
                "time": datetime.datetime.utcnow().isoformat(),
                **check,
            }
        },
    )
