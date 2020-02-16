# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/Colin-b/healthpy/compare/v1.8.0...HEAD
[1.8.0]: https://github.com/Colin-b/healthpy/compare/v1.7.0...v1.8.0
[1.7.0]: https://github.com/Colin-b/healthpy/releases/tag/v1.7.0
