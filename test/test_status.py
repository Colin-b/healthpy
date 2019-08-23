import healthpy


def test_status_aggregation_with_failure():
    assert healthpy.status("pass", "fail", "warn") == "fail"


def test_status_aggregation_with_warning():
    assert healthpy.status("pass", "warn", "pass") == "warn"


def test_status_aggregation_with_pass():
    assert healthpy.status("pass", "pass", "pass") == "pass"
