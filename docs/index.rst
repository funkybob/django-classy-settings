.. Django Classy Settings documentation master file, created by
   sphinx-quickstart on Thu Jul 24 13:53:10 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Django Classy Settings
======================

.. rubric:: Stay classy, Django.

Overview
--------

Class-based settings make it easy for you to manage multiple settings profiles
for your Django project, without ever copying values.

Interdependant values, values sourced from the env, even calculated values are
no problem, since you have the full power of Python and its classes.


Contents
--------

.. toctree::
   :maxdepth: 2

   tips
   simple
   api
   changelog

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


Next, because ``cbs.env`` is also a decorator factory, you can create
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


Also, you can pass a type casting callable to convert the string to whatever
you need, as well as affect validation.  Built in is ``as_bool`` to
intelligently cast value to bool.

.. code-block:: python

   class BaseSettings(cbs.BaseSettings):

       @cbs.env(type=int)
       def COUNT_LIMIT(self):
           return 6

As an additional helper, there is ``cbs.envbool`` which subclasses ``cbs.env``
and sets `type` to ``as_bool``.

Once the value is stripped and lower-cased, ``as_bool`` tests it against two
lists:

True::

    'y', 'yes', 'on', 't', 'true', '1'

False::

    'n', 'no', 'off', 'f', 'false', '0'

Any other value will raise a ValueError.


Feature Toggles
---------------

As a final helper, there's a context processor for adding settings.TOGGLES to
the context, and a function to product a dict of values with defaults.

This is intended to ease addition of feature toggles to your app, controlled by
environment variables.

.. code-block:: python

   import cbs
   from cbs.toggle import toggles

   class BaseSettings(csb.BaseSettings):

       def TOGGLES(self):
           return toggles(FEATURE_ONE=True, PAY_FOR_FEATURE=False)

       @property
       def CONTEXT_PROCESSORS(self):
           return super(BaseSettings).CONTEXT_PROCESSORS + [
               'cbs.context_processors.toggles',
           ]

This will produce a dict containing a key for each argument.  The value will be
from os.environ['TOGGLE_{key}'] if it exists, passed through ``as_bool``, or
the value if it is not set.


Base classes
------------

The `BaseSettings` class is automatically chosen based on the installed version of Django.  You can override this by explicitly choosing the verison base:

- cbs.base.django16.Base16Settings
- cbs.base.django17.Base17Settings
- cbs.base.django18.Base18Settings


Also included is `GlobalSettings`, which pulls in all the default "global" settings from the currently installed version of Django.  This makes it simpler to extend the default settings not included when you run `django-admin startproject`.

.. note::  This class should always be _last_ in your inheritance list.

   .. code-block:: python

      import cbs

      class Settings(cbs.BaseSettings, cbs.GlobalSettings):
          ...
