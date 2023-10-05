import os

__all__ = ['BaseSettings']


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
        :return: functions suitable for module-level ``__getattr__`` and
            ``__dir__``
        """
        base = os.environ.get(env, "")
        name = f"{base.title()}Settings"

        Settings = cls.__children[name]

        return (
            Settings.getattr_factory(),
            Settings.dir_factory(),
        )

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

    @classmethod
    def dir_factory(cls):
        """Returns a function to be used as __dir__ in a module.

        :return: function suitable for module-level ``__dir__``
        """
        from inspect import getmodule

        pkg = getmodule(cls)

        def __dir__(pkg=pkg):
            return [
                x for x in vars(pkg).keys() if x.isupper()
            ] + [
                x for x in dir(cls) if x.isupper()
            ]

        return __dir__
