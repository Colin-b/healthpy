<h2 align="center">API Health Checks</h2>

<p align="center">
<a href="https://github.com/ambv/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href='https://pse.tools.digital.engie.com/drm-all.gem/job/team/view/Python%20modules/job/healthpy/job/master/'><img src='https://pse.tools.digital.engie.com/drm-all.gem/buildStatus/icon?job=team/healthpy/master'></a>
</p>

## HTTP

```python
import healthpy.http

status, details = healthpy.http.check("service name", "http://service_url")
```

## Redis

```python
import healthpy.redis

status, details = healthpy.redis.check("redis://redis_url", "redis_key")
```

## Compute status from multiple statuses

```python
import healthpy

status1 = None 
status2 = None
statusN = None

status = healthpy.status(status1, status2, statusN)
```
