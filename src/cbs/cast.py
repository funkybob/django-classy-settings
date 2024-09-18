"""Type-casting helper functions."""


def as_bool(value: str) -> bool:
    """Smart cast value to bool

    :param str value: Value to cast.
        Value will be stripped and ``.lower()``.
        True values: ``("y", "yes", "on", "t", "true", "1")``
        False values: ``("n", "no", "off", "f", "false", "0")``
        All other values raise a ``ValueError``
    """
    if isinstance(value, bool):
        return value
    value = value.strip().lower()
    if value in ("y", "yes", "on", "t", "true", "1"):
        return True
    if value in ("n", "no", "off", "f", "false", "0"):
        return False
    raise ValueError(f"Unrecognised value for bool: {value !r}")


def as_list(value: str) -> list:
    """
    Smart cast value to list by splitting the input on ",".
    """
    if isinstance(value, list):
        return value
    return [x.strip() for x in value.split(",") if x.strip()]


def as_tuple(value: str) -> tuple:
    """
    Smart cast value to tuple by splitting the input on ",".
    """
    if isinstance(value, tuple):
        return value
    return tuple(as_list(value))
