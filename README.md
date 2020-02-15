<h2 align="center">API Health Checks</h2>

<p align="center">
<a href="https://pypi.org/project/healthpy/"><img alt="pypi version" src="https://img.shields.io/pypi/v/healthpy"></a>
<a href="https://travis-ci.com/Colin-b/healthpy"><img alt="Build status" src="https://api.travis-ci.com/Colin-b/healthpy.svg?branch=develop"></a>
<a href="https://travis-ci.com/Colin-b/healthpy"><img alt="Coverage" src="https://img.shields.io/badge/coverage-100%25-brightgreen"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://travis-ci.com/Colin-b/healthpy"><img alt="Number of tests" src="https://img.shields.io/badge/tests-39 passed-blue"></a>
<a href="https://pypi.org/project/healthpy/"><img alt="Number of downloads" src="https://img.shields.io/pypi/dm/healthpy"></a>
</p>

Health checks are based on [Health Check RFC](https://inadarei.github.io/rfc-healthcheck/) draft version 4.

## HTTP

[requests](https://pypi.python.org/pypi/requests) module must be installed to perform HTTP health checks.

```python
import healthpy.http

status, details = healthpy.http.check("service name", "http://service_url")
```

## Redis

[redis](https://pypi.python.org/pypi/redis) module must be installed to perform Redis health checks.

```python
import healthpy.redis

status, details = healthpy.redis.check("redis://redis_url", "redis_key")
```

## Compute status from multiple statuses

```python
import healthpy

status1 = healthpy.pass_status 
status2 = healthpy.warn_status
statusN = healthpy.fail_status

status = healthpy.status(status1, status2, statusN)
```

## Using custom status

By default pass status is "pass", warn status is "warn" and fail status is "fail".

It can be tweaked by setting the value of healthpy.*_status as in the following sample:

```python
import healthpy

healthpy.pass_status = "ok"
healthpy.warn_status = "custom"
healthpy.fail_status = "error"
```

## Testing

A `pytest` fixture can be used to mock the datetime returned in http health check.

```python
from healthpy.testing import mock_http_health_datetime

def test_http(mock_http_health_datetime):
    pass  # Add your test calling healthpy.http.check
```

## How to install
1. [python 3.6+](https://www.python.org/downloads/) must be installed
2. Use pip to install module:
```sh
python -m pip install healthpy
```
