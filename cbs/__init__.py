import os
from functools import partial

from django.utils.functional import cached_property

from . import cast
from .urls import parse_dburl


class env:
    """property to make environment variable based settings simpler.

    :param Any default: default value
        If it's a string, it will be passed to the ``cast`` function
        When used as a decorator, this is the method.
    :param str key: Override environment variable name
        (Defaults to class attribute name)
    :param str prefix: Prefix to ``key`` when looking up ``os.environ``
    :param func cast: Function to cast ``str`` values.

    """

    def __new__(cls, *args, **kwargs):
        """
        Catch case when we're used as a decorator with keyword arguments, or
        used to pre-set some defaults.
        """
        if not args:
            return partial(cls, **kwargs)
        return object.__new__(cls)

    def __init__(self, getter, key=None, cast=None, prefix=None):
        self.cast = cast

        self.prefix = prefix or ""

        self.key = key

        if callable(getter):
            self.getter = getter
            if not key:
                key = getter.__name__
        else:
            self.getter = None
            self.default = getter

    @cached_property
    def env_name(self):
        return "".join([self.prefix, self.key])

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
                value = self.default
            else:
                value = self.getter(obj)

        if self.cast and isinstance(value, str):
            value = self.cast(value)

        obj.__dict__[self.key] = value
        return value

    @classmethod
    def bool(cls, *args, **kwargs):
        """Helper for bool-cast settings.

        Uses :py:func:`.cast.to_bool`
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


# Target supported env types:
# + str : noop
# + int : int()
# + bool: as_bool
# + list<str>
# - list<int>
# + tuple<str>
# + DB Config: db-url
# - Cache Config: db-url


class BaseSettings:
    """Base class for env switchable settings configuration."""

    __children = {}

    def __init_subclass__(cls, **kwargs):
        cls.__children[cls.__name__] = cls
        super().__init_subclass__(**kwargs)

    @classmethod
    def use(cls, env="DJANGO_MODE"):
        """Helper for accessing sub-classes via env var name.

        Takes the value of ``os.environ[env]``, calls ``.title()`` on it, then
        appends `"Settings"`.

        It will then find a sub-class of that name, and call
        ``getattr__factory`` on it.

        :param str env: Envirionment variable to get settings mode name from.
        :return: function suitable for module-level ``__getattr__``
        """
        base = os.environ.get(env, "")
        name = f"{base.title()}Settings"
        return cls.__children[name].getattr_factory()

    @classmethod
    def getattr_factory(cls):
        """Returns a function to be used as __getattr__ in a module.

        :return: function suitable for module-level ``__getattr__``
        """
        self = cls()

        def __getattr__(key, self=self):
            if not key.isupper():
                raise AttributeError(key)
            val = getattr(self, key)
            if callable(val):
                val = val()
            return val

        return __getattr__
