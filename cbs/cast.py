"""Type-casting helper functions.
"""


def as_bool(value: str) -> bool:
    """Smart cast value to bool

    :param str value: Value to cast.
        Value will be stripped and ``.lower()``.
        Values in ``("y", "yes", "on", "t", "true", "1")`` will be treated as True
        Values in ``("n", "no", "off", "f", "false", "0")`` will be treated as False
        All other values raise a ``ValueError``
    """
    if isinstance(value, bool):
        return value
    value = value.strip().lower()
    if value in ("y", "yes", "on", "t", "true", "1"):
        return True
    if value in ("n", "no", "off", "f", "false", "0"):
        return False
    raise ValueError("Unrecognised value for bool: %r" % value)


def as_list(value: str) -> list:
    """
    Smart cast value to list by splittng the input on ",".
    """
    if isinstance(value, list):
        return value
    return [x.strip() for x in value.split(",") if x.strip()]


def as_tuple(value: str) -> tuple:
    """
    Smart cast value to tuple by splittng the input on ",".
    """
    if isinstance(value, tuple):
        return value
    return tuple(as_list(value))
