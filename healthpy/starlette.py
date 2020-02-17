from typing import Callable

from starlette.applications import Starlette
from starlette.responses import JSONResponse

import healthpy
from healthpy._response import response_body, consul_response_status_code


def add_consul_health_endpoint(app: Starlette, health_check: Callable, **kwargs):
    """
    Create /health: Consul Health check endpoint implementing https://inadarei.github.io/rfc-healthcheck/ but following
    Consul expected status code (https://www.consul.io/docs/agent/checks.html).

    :param app: The ASGI application.
    :param health_check: async callable returning a tuple of size 2 with a string providing the status (pass, warn, fail)
    and the "Checks object" as a dictionary as per https://inadarei.github.io/rfc-healthcheck/
    :param version: (optional) public version of the service. If not provided, version will be extracted from the
    release_id, considering that release_id is following semantic versioning.
    Version will be considered as the MAJOR component of a MAJOR.MINOR.PATCH release_id.
    :param release_id: (optional) in well-designed APIs, backwards-compatible changes in the service
    should not update a version number. APIs usually change their version number as infrequently as possible,
    to preserve stable interface. However, implementation of an API may change much more frequently,
    which leads to the importance of having separate “release number” or “releaseId”
    that is different from the public version of the API.
    :param notes: (optional) array of notes relevant to current state of health.
    :param links: (optional) is an object containing link relations and URIs [RFC3986]
    for external links that MAY contain more information about the health of the endpoint.
    All values of this object SHALL be URIs. Keys MAY also be URIs.
    Per web-linking standards [RFC8288] a link relationship SHOULD either be a common/registered one
    or be indicated as a URI, to avoid name clashes.
    If a “self” link is provided, it MAY be used by clients to check health via HTTP response code, as mentioned above.
    :param service_id: (optional) is a unique identifier of the service, in the application scope.
    :param description: (optional) is a human-friendly description of the service.
    """

    @app.route("/health")
    async def health(request):
        """
        responses:
            200:
                description: "Server is in a coherent state."
                schema:
                    required:
                        - checks
                        - releaseId
                        - status
                        - version
                    properties:
                        status:
                            type: string
                            description: "Indicates whether the service status is acceptable or not."
                            example: pass
                            enum:
                                - pass
                        version:
                            type: string
                            description: "Public version of the service."
                            example: "1"
                        releaseId:
                            type: string
                            description: "Version of the service."
                            example: "1.0.0"
                        checks:
                            type: object
                            description: "Provides more details about the status of the service."
                    type: object
            429:
                description: "Server is almost in a coherent state."
                schema:
                    required:
                        - checks
                        - releaseId
                        - status
                        - version
                    properties:
                        status:
                            type: string
                            description: "Indicates whether the service status is acceptable or not."
                            example: warn
                            enum:
                                - warn
                        version:
                            type: string
                            description: "Public version of the service."
                            example: "1"
                        releaseId:
                            type: string
                            description: "Version of the service."
                            example: "1.0.0"
                        checks:
                            type: object
                            description: "Provides more details about the status of the service."
                    type: object
            400:
                description: "Server is not in a coherent state."
                schema:
                    required:
                        - checks
                        - releaseId
                        - status
                        - version
                    properties:
                        status:
                            type: string
                            description: "Indicates whether the service status is acceptable or not."
                            example: fail
                            enum:
                                - fail
                        version:
                            type: string
                            description: "Public version of the service."
                            example: "1"
                        releaseId:
                            type: string
                            description: "Version of the service."
                            example: "1.0.0"
                        checks:
                            type: object
                            description: "Provides more details about the status of the service."
                        output:
                            type: string
                            description: "Raw error output."
                    type: object
        summary: "Check service health"
        description: "This endpoint perform a quick server state check."
        operationId: get_health
        tags:
            - Monitoring
        """
        try:
            status, checks = await health_check()
            body = response_body(status, checks=checks, **kwargs)
        except Exception as e:
            status = healthpy.fail_status
            body = response_body(status, output=str(e), **kwargs)
        return JSONResponse(
            body,
            status_code=consul_response_status_code(status),
            media_type="application/health+json",
        )
