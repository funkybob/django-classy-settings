.. Django Classy Settings documentation master file, created by
   sphinx-quickstart on Thu Jul 24 13:53:10 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Django Classy Settings
======================

.. rubric:: Stay classy, Django.

Overview
--------

Class-based settings make it easy for you to manage multiple settings for your
Django project, without ever copying values.

Interdependant values, values sourced from the env, even calculated values are
no problem, since you have the full power of Python and its classes.


Contents
--------

.. toctree::
   :maxdepth: 2

   tips
   simple

Quickstart
----------

Replace your default ``settings.py``:

.. code-block:: python

    import cbs

    class BaseSettings(cbs.BaseSettings):
        PROJECT_NAME = 'myproject'

You must provide the project name you passed to 'startproject'.

Derive testing/staging/production settings:

.. code-block:: python

    class LocalSettings(BaseSettings):
        ...

    class StagingSettings(BaseSettings):
        STATIC_ROOT = '....'

    class ProductionSettings(StagingSettings):
        DEBUG = False

Any upper-case properties will be included in your settings.  Any methods which
match this will be called to yield their values.

Finally, apply the setting you want:

.. code-block:: python

    import os
    MODE = os.environ.get('DJANGO_MODE', 'Local')
    cbs.apply('{}Settings'.format(MODE.title()), globals())


Helpers
-------

We all like moving settings into the ENV, right?  So, here's a helper.

.. code-block:: python

    class Settings(BaseSettings):

        # Will return 'SECRET' from env vars, or the default if not set.
        @cbs.env
        def SECRET(self):
            return 'default-dummy-secret'

        # We can define which env var to get the value from
        @cbs.env(key='DJANGO_SECRET')
        def SECRET(self):
            return 'default-dummy-secret'

        # Or just set a prefix
        @cbs.env(prefix='DJANGO_')
        def SECRET(self):
            return 'default-dummy-secret'

You can override the default prefix of '' by setting ``cbs.DEFAULT_ENV_PREFIX``

.. code-block:: python

   import cbs

   cbs.DEFAULT_ENV_PREFIX = 'DJANGO_'

   class Settings(BaseSettings):
       @cbs.env
       def SECRET(self):
           '''Gets its value from os.environ['DJANGO_SECRET']'''
            return 'dummy-secret'


The recommended pattern for env settings that are required is to raise
``django.core.exceptions.ImproperlyConfigured``:

.. code-block:: python

   import cbs

   class Settings(BaseSettings):
       @cbs.env
       def SECRET(self):
           raise ImproperlyConfigured('You must specify SECRET in env')


Finally, because ``cbs.env`` is also a decorator factory, you can create
decorators for each prefix you need, if you have many.

.. code-block:: python

   denv = cbs.env(prefix='DJANGO_')
   ppenv = cbs.env(prefix='PAYPAL_')

   class BaseSettings(cbs.BaseSettings):
       @denv
       def SECRET(self):
           return 'dummy-secret'

       @ppenv
       def API_USERNAME(self):
           return 'test@paypal.com'

