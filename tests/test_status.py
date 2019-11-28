import healthpy


def test_status_aggregation_with_failure():
    assert healthpy.status("pass", "fail", "warn") == "fail"


def test_status_aggregation_with_warning():
    assert healthpy.status("pass", "warn", "pass") == "warn"


def test_status_aggregation_with_pass():
    assert healthpy.status("pass", "pass", "pass") == "pass"


def test_status_aggregation_with_custom_failure(monkeypatch):
    monkeypatch.setattr(healthpy, "fail_status", "custom")
    assert healthpy.status("pass", "custom", "warn") == "custom"


def test_status_aggregation_with_custom_warning(monkeypatch):
    monkeypatch.setattr(healthpy, "warn_status", "custom")
    assert healthpy.status("pass", "custom", "pass") == "custom"


def test_status_aggregation_with_custom_pass(monkeypatch):
    monkeypatch.setattr(healthpy, "pass_status", "custom")
    assert healthpy.status("custom", "custom", "custom") == "custom"


def test_default_pass_status():
    assert healthpy.pass_status == "pass"


def test_default_warn_status():
    assert healthpy.warn_status == "warn"


def test_default_fail_status():
    assert healthpy.fail_status == "fail"
