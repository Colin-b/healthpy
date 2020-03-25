import datetime
import re
from typing import List, Any, Optional

import healthpy


def _is_json(content_type: Optional[str]) -> bool:
    return re.match(r"application/(health\+)?json", content_type or "")


def _api_health_status(health_response: Any) -> str:
    if isinstance(health_response, dict):
        return health_response.get("status", healthpy.pass_status)
    return healthpy.pass_status


def _check(
    service_name: str,
    url: str,
    request_class,
    status_extracting: callable = None,
    failure_status: str = None,
    affected_endpoints: List[str] = None,
    additional_keys: dict = None,
    **kwargs,
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
    try:
        request = request_class(url, **kwargs)
        if request.is_error():
            status = failure_status or healthpy.fail_status
            check = (
                {"output": request.content()} if status != healthpy.pass_status else {}
            )
        else:
            if not status_extracting:
                status_extracting = _api_health_status

            response = request.content()
            status = status_extracting(response)
            check = {"observedValue": response}
    except Exception as e:
        status = failure_status or healthpy.fail_status
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
