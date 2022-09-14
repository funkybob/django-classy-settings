django-classy-settings
======================

Minimalist approach to class-based settings for Django

https://django-classy-settings.readthedocs.io/en/latest/


Quick Start
-----------

In your `settings.py`

    from cbs import BaseSettings, env


    ...
    # For env settings with a DJANGO_ prefix
    denv = env['DJANGO_']

    class Settings(BaseSettings):

        DEBUG = denv.bool(True)  # Controlled by DJANGO_DEBUG env var

        DEFAULT_DATABASE = denv.dburl('sqlite://db.sqlite')

        def DATABASES(self):
            return {
                'default': self.DEFAULT_DATABASE,
            }


    class ProdSettings(Settings):
        DEBUG = False

        @env
        def STATIC_ROOT(self):
            raise ValueError("Must set STATIC_ROOT!")

    __getattr__, __dir__ = BaseSettings.use()


Switch between ``Settings`` and ``ProdSettings`` using the ``DJANGO_MODE`` env var:

    # Run default Settings
    $ ./manage.py test

    # Run ProdSettings
    $ DJANGO_MODE=prod ./manage.py test
