<h2 align="center">Health Check for HTTP APIs</h2>

<p align="center">
<a href="https://pypi.org/project/healthpy/"><img alt="pypi version" src="https://img.shields.io/pypi/v/healthpy"></a>
<a href="https://travis-ci.com/Colin-b/healthpy"><img alt="Build status" src="https://api.travis-ci.com/Colin-b/healthpy.svg?branch=develop"></a>
<a href="https://travis-ci.com/Colin-b/healthpy"><img alt="Coverage" src="https://img.shields.io/badge/coverage-100%25-brightgreen"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://travis-ci.com/Colin-b/healthpy"><img alt="Number of tests" src="https://img.shields.io/badge/tests-69 passed-blue"></a>
<a href="https://pypi.org/project/healthpy/"><img alt="Number of downloads" src="https://img.shields.io/pypi/dm/healthpy"></a>
</p>

Create an health check endpoint on your REST API following [Health Check RFC](https://inadarei.github.io/rfc-healthcheck/) draft version 4.

- [Perform checks](#perform-checks)
  - [Of an external HTTP resource](#http)
  - [Of a redis server](#redis)
- [Return health check result](#return-result)
  - [Aggregate multiple statuses](#compute-status-from-multiple-statuses)
  - [Use a custom status](#using-custom-status)
  - [HTTP response body](#http-response-body)
  - [HTTP response status code](#http-response-status-code)
- [Endpoint](#endpoint)
  - [Starlette](#starlette)

## Perform checks

In case you have external dependencies, you should check the health of those dependencies.

### HTTP

If you have an external HTTP resource, you can check its health,as in the following sample:

```python
import healthpy.http

status, checks = healthpy.http.check("petstore", "https://petstore3.swagger.io/api/v3/openapi.json")
```

Note: [requests](https://pypi.python.org/pypi/requests) module must be installed to perform HTTP health checks.

### Redis

If you rely on redis, you should check its health.

[redis](https://pypi.python.org/pypi/redis) module must be installed to perform Redis health checks.

```python
import healthpy.redis

status, checks = healthpy.redis.check("redis://redis_url", "redis_key")
```

## Return result

Once all checks have been performed you should return the result to your client.

### Compute status from multiple statuses

If you performed more than one check, you have to compute an aggregated status from all the checks.

```python
import healthpy

status1 = healthpy.pass_status 
status2 = healthpy.warn_status
statusN = healthpy.fail_status

status = healthpy.status(status1, status2, statusN)
```

### Using custom status

By default pass status is "pass", warn status is "warn" and fail status is "fail".

It can be tweaked by setting the value of healthpy.*_status as in the following sample:

```python
import healthpy

healthpy.pass_status = "ok"
healthpy.warn_status = "custom"
healthpy.fail_status = "error"
```

### HTTP response body

HTTP response body can be retrieved as a dictionary to be returned as JSON.

```python
import healthpy

status = healthpy.pass_status  # replace with the aggregated status
checks = {}  # replace with the computed checks

body = healthpy.response_body(status, checks=checks)
```

Checks results are not mandatory in the response.

```python
import healthpy

status = healthpy.pass_status  # replace with the aggregated status

body = healthpy.response_body(status)
```

### HTTP response status code

HTTP response status code can be retrieved as an integer.

```python
import healthpy

status = healthpy.pass_status  # replace with the aggregated status

status_code = healthpy.response_status_code(status)
```

#### Consul

HTTP response status code should be a bit different for [Consul](https://www.consul.io/docs/agent/checks.html) health checks.

```python
import healthpy

status = healthpy.pass_status  # replace with the aggregated status

status_code = healthpy.consul_response_status_code(status)
```

## Endpoint

### Starlette

An helper function is available to create a [starlette](https://www.starlette.io) endpoint for [Consul](https://www.consul.io/docs/agent/checks.html) health check.

```python
from starlette.applications import Starlette
import healthpy
import healthpy.http
import healthpy.redis
from healthpy.starlette import add_consul_health_endpoint


app = Starlette()


async def health_check():
    # TODO Replace by your own checks.
    status_1, checks_1 = healthpy.http.check("my external dependency", "http://url_to_check")
    status_2, checks_2 = healthpy.redis.check("redis://redis_url", "key_to_check")
    return healthpy.status(status_1, status_2), {**checks_1, **checks_2}

# /health endpoint will call the health_check coroutine.
add_consul_health_endpoint(app, health_check)
```

Note: [starlette](https://pypi.python.org/pypi/starlette) module must be installed.

## Testing

A `pytest` fixture can be used to mock the datetime returned in http health check.

```python
from healthpy.testing import mock_http_health_datetime

def test_http(mock_http_health_datetime):
    # Time will be returned as "2018-10-11T15:05:05.663979"
    pass  # Add your test calling healthpy.http.check
```

## How to install
1. [python 3.6+](https://www.python.org/downloads/) must be installed
2. Use pip to install module:
```sh
python -m pip install healthpy
```
