import os

__all__ = ['BaseSettings']


class BaseSettings:
    """Base class for env switchable settings configuration."""

    __children = {}

    def __init_subclass__(cls, **kwargs):
        cls.__children[cls.__name__] = cls
        super().__init_subclass__(**kwargs)

    def __getattribute__(self, name):
        val = super().__getattribute__(name)
        if name.isupper() and callable(val):
            val = val()
        return val

    @classmethod
    def use(cls, env="DJANGO_MODE", env_path=None):
        """Helper for accessing sub-classes via env var name.

        Gets a sub-class instance using ``get_settings_instance``, and returns
        the results of calling ``getattr__factory`` and ``dir_factory`` on it.

        :param str env: Environment variable to get settings mode name from.
        :param str env_path: the path to the file containing the environment variable, if left empty, os.environ will be used instead.
        :return: functions suitable for module-level ``__getattr__`` and
            ``__dir__``
        """
        settings = cls.get_settings_instance(env, env_path)

        return (
            settings.getattr_factory(),
            settings.dir_factory(),
        )

    @classmethod
    def get_settings_instance(cls, env="DJANGO_MODE", env_path=None):
        """Create an instance of the appropriate Settings sub-class.

        Takes the value of ``os.environ[env]``, calls ``.title()`` on it,
        or reads the value from the specified file in ``env_path``,
        then appends `"Settings"`.

        It will then find a sub-class of that name, and return an instance of
        it.

        """
        base = os.environ.get(env, "")

        if env_path:
            try:
                import eniron
            except ImportError:
                raise ImportError(
                    "if you want to read your environment variables from a file, "
                    "you need to install the optional `django-environ` package"
                    "try `pip install django-classy-settings[environ]`"
                )

            if os.path.exists(env_path):
                env = environ.Env()
                env.read_env(env_path)
                base = env.str(env)

        name = f"{base.title()}Settings"

        try:
            return cls.__children[name]()
        except KeyError:
            raise ValueError(
                f'Could not find Settings class for mode {base!r} '
                f'(Known: {", ".join(cls.__children)})',
            )

    def getattr_factory(self):
        """Returns a function to be used as __getattr__ in a module.

        :return: function suitable for module-level ``__getattr__``
        """
        def __getattr__(key, self=self):
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

        def __dir__(pkg=pkg):
            return [
                x for x in vars(pkg).keys() if x.isupper()
            ] + [
                x for x in dir(self) if x.isupper()
            ]

        return __dir__
