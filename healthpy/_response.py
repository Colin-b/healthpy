import healthpy


def response_body(status: str, **kwargs) -> dict:
    """
    Health Check Response Format for HTTP APIs uses the JSON format described in [RFC8259]
    and has the media type “application/health+json”.

    This function return a dict that can be returned as JSON.

    :param status: (required) indicates whether the service status is acceptable or not.
    The value of the status field is case-insensitive.
    :param version: (optional) public version of the service. If not provided, version will be extracted from the
    release_id, considering that release_id is following semantic versioning.
    Version will be considered as the MAJOR component of a MAJOR.MINOR.PATCH release_id.
    :param release_id: (optional) in well-designed APIs, backwards-compatible changes in the service
    should not update a version number. APIs usually change their version number as infrequently as possible,
    to preserve stable interface. However, implementation of an API may change much more frequently,
    which leads to the importance of having separate “release number” or “releaseId”
    that is different from the public version of the API.
    :param notes: (optional) array of notes relevant to current state of health.
    :param output: (optional) raw error output, in case of “fail” or “warn” states.
    This field SHOULD be omitted for “pass” state.
    :param checks: (optional) is an object that provides detailed health statuses of additional downstream systems
    and endpoints which can affect the overall health of the main API.
    :param links: (optional) is an object containing link relations and URIs [RFC3986]
    for external links that MAY contain more information about the health of the endpoint.
    All values of this object SHALL be URIs. Keys MAY also be URIs.
    Per web-linking standards [RFC8288] a link relationship SHOULD either be a common/registered one
    or be indicated as a URI, to avoid name clashes.
    If a “self” link is provided, it MAY be used by clients to check health via HTTP response code, as mentioned above.
    :param service_id: (optional) is a unique identifier of the service, in the application scope.
    :param description: (optional) is a human-friendly description of the service.
    """
    body = {"status": status}

    release_id = kwargs.pop("release_id", None)
    if release_id:
        kwargs["releaseId"] = release_id
        kwargs["version"] = kwargs.pop("version", release_id.split(".", maxsplit=1)[0])

    if "service_id" in kwargs:
        kwargs["serviceId"] = kwargs.pop("service_id")

    body.update(kwargs)
    return body


def response_status_code(status: str) -> int:
    """
    HTTP response code returned by the health endpoint.
    For “pass” status, HTTP response code in the 2xx-3xx range MUST be used (200 will be used).
    For “fail” status, HTTP response code in the 4xx-5xx range MUST be used (400 will be used).
    In case of the “warn” status, endpoints MUST return HTTP status in the 2xx-3xx range (200 will be used),
    and additional information SHOULD be provided, utilizing optional fields of the response.

    :param status: Status of the application.
    :return: HTTP status code to return to the client.
    """
    return 400 if healthpy.fail_status == status else 200


def consul_response_status_code(status: str) -> int:
    """
    HTTP response code returned by the health endpoint.
    That should be returned if the client is Consul.

    More information on Consul health checks can be found here: https://www.consul.io/docs/agent/checks.html

    For “pass” status, HTTP response code 200 is returned.
    For “fail” status, HTTP response code 400 is returned.
    In case of the “warn” status, HTTP response code 429 is returned.

    :param status: Status of the application.
    :return: HTTP status code to return to Consul.
    """
    if healthpy.fail_status == status:
        return 400  # Consul consider every non 429 or 2** as Critical
    if healthpy.warn_status == status:
        return 429  # Consul consider a 429 as a Warning
    return 200  # Consul consider every 2** as Ok
