# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.11.1] - 2020-07-27
### Fixed
- error_status_extracting is now used to extract the status to return in case of failure as well. (default to failure_status)

### Changed
- The parameter provided to error_status_extracting will be `None` in case of a failure.

## [1.11.0] - 2020-03-26
### Added
- Allow to provide a custom way to resolve status in case of HTTP error via `error_status_extracting` parameter.

### Deprecated
- `failure_status` parameter to be used in case of HTTP error. Use `error_status_extracting` parameter instead.

### Changed
- In case of HTTP error, try to extract status from HTTP body before considering status as fail.

## [1.10.0] - 2020-03-25
### Added
- Allow to use [`httpx`](https://pypi.python.org/pypi/httpx) instead of [`requests`](https://pypi.python.org/pypi/requests) to perform HTTP health check.

### Changed
- In case an HTTP error occurred, output will be returned as JSON interpreted if possible instead of string.

## [1.9.0] - 2020-02-17
### Added
- `healthpy.starlette.add_consul_health_endpoint` function to add a [Consul](https://www.consul.io/docs/agent/checks.html) health check endpoint to a [Starlette](https://www.starlette.io) application.

## [1.8.0] - 2020-02-16
### Changed
- Update to latest RFC specification (draft v4) meaning:
    - affectedEndpoints is not sent anymore in case status is pass.
    - output is not sent anymore in case status is pass.
    - additional keys can now be provided.

### Added
- `healthpy.response_body` function to retrieve a dict to return as JSON to the client.
- `healthpy.response_status_code` function to retrieve an HTTP status code to return to the client.
- `healthpy.consul_response_status_code` function to retrieve an HTTP status code to return to Consul.

### Fixed
- affectedEndpoints is not sent anymore if not provided.

### Deprecated
- Providing non mandatory parameters via positional arguments will be removed in the next major release.

## [1.7.0] - 2019-11-29
### Added
- Public release.

[Unreleased]: https://github.com/Colin-b/healthpy/compare/v1.11.1...HEAD
[1.11.1]: https://github.com/Colin-b/healthpy/compare/v1.11.0...v1.11.1
[1.11.0]: https://github.com/Colin-b/healthpy/compare/v1.10.0...v1.11.0
[1.10.0]: https://github.com/Colin-b/healthpy/compare/v1.9.0...v1.10.0
[1.9.0]: https://github.com/Colin-b/healthpy/compare/v1.8.0...v1.9.0
[1.8.0]: https://github.com/Colin-b/healthpy/compare/v1.7.0...v1.8.0
[1.7.0]: https://github.com/Colin-b/healthpy/releases/tag/v1.7.0
