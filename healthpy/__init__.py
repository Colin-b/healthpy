from healthpy._status import status
from healthpy._response import (
    response_body,
    response_status_code,
    consul_response_status_code,
)
from healthpy.version import __version__

# API publishers SHOULD use following values for the field:
# “pass”: healthy (acceptable aliases: “ok” to support Node’s Terminus and “up” for Java’s SpringBoot)
pass_status = "pass"

# API publishers SHOULD use following values for the field:
# “warn”: healthy, with some concerns.
warn_status = "warn"

# API publishers SHOULD use following values for the field:
# “fail”: unhealthy (acceptable aliases: “error” to support Node’s Terminus and “down” for Java’s SpringBoot)
fail_status = "fail"
