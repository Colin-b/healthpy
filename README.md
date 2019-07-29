<h2 align="center">API Health Checks</h2>

<p align="center">
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href='https://pse.tools.digital.engie.com/drm-all.gem/job/team/view/Python%20modules/job/healthpy/job/master/'><img src='https://pse.tools.digital.engie.com/drm-all.gem/buildStatus/icon?job=team/healthpy/master'></a>
<a href='https://pse.tools.digital.engie.com/drm-all.gem/job/team/view/Python%20modules/job/healthpy/job/master/cobertura/'><img src='https://pse.tools.digital.engie.com/drm-all.gem/buildStatus/icon?job=team/healthpy/master&config=testCoverage'></a>
<a href='https://pse.tools.digital.engie.com/drm-all.gem/job/team/view/Python%20modules/job/healthpy/job/master/lastSuccessfulBuild/testReport/'><img src='https://pse.tools.digital.engie.com/drm-all.gem/buildStatus/icon?job=team/healthpy/master&config=testCount'></a>
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

## How to install
1. [python 3.7+](https://www.python.org/downloads/) must be installed
2. Use pip to install module:
```sh
python -m pip install healthpy -i https://all-team-remote:tBa%40W%29tvB%5E%3C%3B2Jm3@artifactory.tools.digital.engie.com/artifactory/api/pypi/all-team-pypi-prod/simple
```
