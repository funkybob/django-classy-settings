
import os
from functools import cached_property, partial

from . import cast
from .urls import parse_dburl

DEFAULT_ENV_PREFIX = ''


class env:
    '''
    Decorator to make environ based settings simpler.

    @env
    def SOMETHING_KEY(self):
        return 'default'

    You can override the key to use in the env:

    @env(key='OTHER_NAME')
    def SETTINGS_NAME(self):
        ...

    Or, if you want the env to have a prefix not in settings:

    @env(prefix='MY_')
    def SETTING(self):
        ...

    ``key`` and ``prefix`` can be used together.

    You can pass a caster / validator:

    @env(cast=int)
    def SETTING(self):

    Alternatively there are helpers for common castings:

    @env.int
    @env.bool
    @env.dburl
    @env.list

    Additionally, it can be used as a property for immediate values.

    DEBUG = env.bool(True)
    '''
    def __new__(cls, *args, **kwargs):
        if not args:
            return partial(cls, **kwargs)
        return object.__new__(cls)

    def __init__(self, getter, key=None, cast=None, prefix=None):
        '''
        `getter` may be a method, or a constant value
        '''
        self.cast = cast

        if prefix is None:
            prefix = DEFAULT_ENV_PREFIX
        self.prefix = prefix

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
        return ''.join([self.prefix, self.key])

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
        else:
            if self.cast:
                value = self.cast(value)
        obj.__dict__[self.key] = value
        return value

    @classmethod
    def bool(cls, *args, **kwargs):
        return cls(cast=cast.as_bool, *args, **kwargs)

    @classmethod
    def int(cls, *args, **kwargs):
        return cls(cast=int, *args, **kwargs)

    @classmethod
    def dburl(cls, *args, **kwargs):
        return cls(cast=parse_dburl, *args, **kwargs)

    @classmethod
    def list(cls, *args, **kwargs):
        return cls(cast=cast.as_list, *args, **kwargs)

    @classmethod
    def tuple(cls, *args, **kwargs):
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
    __children = {}

    def __init_subclass__(cls, **kwargs):
        cls.__children[cls.__name__] = cls
        super().__init_subclass__(**kwargs)

    @classmethod
    def use(cls, env='DJANGO_MODE'):
        '''Helper for accessing sub-classes via env var name'''
        base = os.environ.get(env, '')
        name = f'{base.title()}Settings'
        return cls.__children[name].getattr_factory()

    @classmethod
    def getattr_factory(cls):
        '''
        Returns a function to be used as __getattr__ in a module.
        '''

        self = cls()
        def __getattr__(key, self=self):
            if not key.isupper():
                raise AttributeError(key)
            val = getattr(self, key)
            if callable(val):
                val = val()
            return val

        return __getattr__
