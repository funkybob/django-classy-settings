import os
from functools import partial

from django.utils.functional import cached_property

from . import cast
from .urls import parse_dburl

__all__ = ["env"]

# Target supported env types:
# + str : noop
# + int : int()
# + bool: as_bool
# + list<str>
# - list<int>
# + tuple<str>
# + DB Config: db-url
# - Cache Config: db-url


class env:  # noqa: N801
    """property to make environment variable based settings simpler.

    :param Any default: default value
        If it's a string, it will be passed to the ``cast`` function
        When used as a decorator, this is the method.
    :param str key: Override environment variable name
        (Defaults to class attribute name)
    :param str prefix: Prefix to ``key`` when looking up ``os.environ``
    :param func cast: Function to cast ``str`` values.

    """

    class Required:
        pass

    PREFIX = ""

    def __new__(cls, *args, **kwargs):
        """
        Catch case when we're used as a decorator with keyword arguments, or
        used to pre-set some defaults.
        """
        if not args and not kwargs:
            raise TypeError("env requires positional or keyword arguments")
        if not args:
            return partial(cls, **kwargs)
        return object.__new__(cls)

    def __class_getitem__(cls, key):
        """Helper to allow creating env sub-classes with PREFIX pre-set."""
        return type(f"{cls.__name__}__{key}", (cls,), {"PREFIX": key})

    def __init__(self, getter, key=None, cast=None, prefix=None):
        self.cast = cast
        self.key = key
        self.prefix = prefix or self.PREFIX

        if getter is not self.Required and callable(getter):
            self.getter = getter
        else:
            self.getter = None
            self.default = getter

    @cached_property
    def env_name(self):
        return f"{self.prefix}{self.key}"

    def __set_name__(self, owner, name):
        if self.key is None:
            self.key = name

    def __get__(self, obj, cls=None):
        if obj is None:
            return self

        try:
            value = os.environ[self.env_name]
        except KeyError:
            if self.getter is None:
                if self.default is self.Required:
                    raise ValueError(f"Environment varariable {self.env_name} is required but not set.")
                value = self.default
            else:
                try:
                    value = self.getter(obj)
                except Exception as e:
                    raise e from None

        if self.cast and isinstance(value, str):
            value = self.cast(value)

        obj.__dict__[self.key] = value
        return value

    def __call__(self):
        return self.__get__(self)

    @classmethod
    def bool(cls, *args, **kwargs):
        """Helper for bool-cast settings.

        Uses :py:func:`.cast.as_bool`
        """
        return cls(cast=cast.as_bool, *args, **kwargs)

    @classmethod
    def int(cls, *args, **kwargs):
        """Helper for int-cast settings.

        Uses ``int``
        """
        return cls(cast=int, *args, **kwargs)

    @classmethod
    def dburl(cls, *args, **kwargs):
        """Helper for DB-Url cast settings.

        Uses :py:func:`.urls.parse_dburl`
        """
        return cls(cast=parse_dburl, *args, **kwargs)

    @classmethod
    def list(cls, *args, **kwargs):
        """Helper for list-cast settings.

        Uses :py:func:`.cast.as_list`
        """
        return cls(cast=cast.as_list, *args, **kwargs)

    @classmethod
    def tuple(cls, *args, **kwargs):
        """Helper for tuple-cast settings.

        Uses :py:func:`.cast.as_tuple`
        """
        return cls(cast=cast.as_tuple, *args, **kwargs)
