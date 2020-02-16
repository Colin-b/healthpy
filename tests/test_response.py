import healthpy


def test_default_pass_response_body():
    assert healthpy.response_body(healthpy.pass_status) == {
        "status": "pass",
    }


def test_default_warn_response_body():
    assert healthpy.response_body(healthpy.warn_status) == {
        "status": "warn",
    }


def test_default_fail_response_body():
    assert healthpy.response_body(healthpy.fail_status) == {
        "status": "fail",
    }


def test_response_body_version():
    assert healthpy.response_body(healthpy.pass_status, version="1") == {
        "status": "pass",
        "version": "1",
    }


def test_response_body_release_id_non_semantic_without_version():
    assert healthpy.response_body(healthpy.pass_status, release_id="1") == {
        "status": "pass",
        "releaseId": "1",
        "version": "1",
    }


def test_response_body_release_id_non_semantic_with_version():
    assert healthpy.response_body(
        healthpy.pass_status, version="2", release_id="1"
    ) == {"status": "pass", "releaseId": "1", "version": "2",}


def test_response_body_release_id_semantic_without_version():
    assert healthpy.response_body(healthpy.pass_status, release_id="1.2.3") == {
        "status": "pass",
        "releaseId": "1.2.3",
        "version": "1",
    }


def test_response_body_release_id_semantic_with_version():
    assert healthpy.response_body(
        healthpy.pass_status, version="2", release_id="1.2.3"
    ) == {"status": "pass", "releaseId": "1.2.3", "version": "2",}


def test_response_body_notes():
    assert healthpy.response_body(healthpy.pass_status, notes=["note 1", "note 2"]) == {
        "status": "pass",
        "notes": ["note 1", "note 2"],
    }


def test_response_body_output():
    assert healthpy.response_body(healthpy.pass_status, output="test output") == {
        "status": "pass",
        "output": "test output",
    }


def test_response_body_checks():
    assert healthpy.response_body(healthpy.pass_status, checks={}) == {
        "status": "pass",
        "checks": {},
    }


def test_response_body_links():
    assert healthpy.response_body(
        healthpy.pass_status, links={"http://key": "http://value"}
    ) == {"status": "pass", "links": {"http://key": "http://value"},}


def test_response_body_service_id():
    assert healthpy.response_body(healthpy.pass_status, service_id="test") == {
        "status": "pass",
        "serviceId": "test",
    }


def test_response_body_description():
    assert healthpy.response_body(
        healthpy.pass_status, description="test description"
    ) == {"status": "pass", "description": "test description",}


def test_pass_response_status_code():
    assert healthpy.response_status_code(healthpy.pass_status) == 200


def test_warn_response_status_code():
    assert healthpy.response_status_code(healthpy.warn_status) == 200


def test_fail_response_status_code():
    assert healthpy.response_status_code(healthpy.fail_status) == 400


def test_unknown_response_status_code():
    assert healthpy.response_status_code("unknown") == 200


def test_pass_consul_response_status_code():
    assert healthpy.consul_response_status_code(healthpy.pass_status) == 200


def test_warn_consul_response_status_code():
    assert healthpy.consul_response_status_code(healthpy.warn_status) == 429


def test_fail_consul_response_status_code():
    assert healthpy.consul_response_status_code(healthpy.fail_status) == 400


def test_unknown_consul_response_status_code():
    assert healthpy.consul_response_status_code("unknown") == 200
