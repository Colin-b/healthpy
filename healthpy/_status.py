def status(*statuses: str) -> str:
    """
    Return status according to statuses:
    fail if there is at least one fail status, warn if there is at least one warn status
    pass otherwise

    :param statuses: List of statuses, valid values are pass, warn or fail
    :return: Status according to statuses
    """
    if "fail" in statuses:
        return "fail"
    if "warn" in statuses:
        return "warn"
    return "pass"
