import os

__all__ = ["BaseSettings"]


class BaseSettings:
    """Base class for env switchable settings configuration."""

    __children = {}  # noqa: RUF012

    def __init_subclass__(cls, **kwargs):
        cls.__children[cls.__name__] = cls
        super().__init_subclass__(**kwargs)

    def __getattribute__(self, name):
        val = super().__getattribute__(name)
        if name.isupper() and callable(val):
            val = val()
        return val

    @classmethod
    def use(cls, env="DJANGO_MODE"):
        """Helper for accessing sub-classes via env var name.

        Gets a sub-class instance using ``get_settings_instance``, and returns
        the results of calling ``getattr_factory`` and ``dir_factory`` on it.

        :param str env: Envirionment variable to get settings mode name from.
        :return: functions suitable for module-level ``__getattr__`` and
            ``__dir__``
        """
        settings = cls.get_settings_instance(env)

        return (
            settings.getattr_factory(),
            settings.dir_factory(),
        )

    @classmethod
    def get_settings_instance(cls, env="DJANGO_MODE"):
        """Create an instance of the appropriate Settings sub-class.

        Takes the value of ``os.environ[env]``, calls ``.title()`` on it, then
        appends `"Settings"`.

        It will then find a sub-class of that name, and return an instance of
        it.

        """
        base = os.environ.get(env, "")
        name = f"{base.title()}Settings"

        try:
            return cls.__children[name]()
        except KeyError:
            raise ValueError(
                f'Could not find Settings class for mode {base!r} ' f'(Known: {", ".join(cls.__children)})',
            )

    def getattr_factory(self):
        """Returns a function to be used as __getattr__ in a module.

        :return: function suitable for module-level ``__getattr__``
        """

        def __getattr__(key, self=self):  # noqa: N807
            if not key.isupper():
                raise AttributeError(key)
            return getattr(self, key)

        return __getattr__

    def dir_factory(self):
        """Returns a function to be used as __dir__ in a module.

        :return: function suitable for module-level ``__dir__``
        """
        from inspect import getmodule

        pkg = getmodule(self.__class__)

        def __dir__(pkg=pkg):  # noqa: N807
            # fmt: off
            return [
                x for x in vars(pkg).keys()
                if x.isupper()
            ] + [
                x for x in dir(self)
                if x.isupper()
            ]
            # fmt: on

        return __dir__
