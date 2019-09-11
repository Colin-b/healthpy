import healthpy


def status(*statuses: str) -> str:
    """
    Return status according to provided statuses:

    Content of healthpy.fail_status if there is at least one fail status
    Content of healthpy.warn_status if there is at least one warn status
    Content of healthpy.pass_status otherwise

    :param statuses: List of statuses, valid values should be amongst the one defined in healthpy.*_status variables.
    :return: Status according to statuses
    """
    if healthpy.fail_status in statuses:
        return healthpy.fail_status
    if healthpy.warn_status in statuses:
        return healthpy.warn_status
    return healthpy.pass_status
