.. Django Classy Settings documentation master file, created by
   sphinx-quickstart on Thu Jul 24 13:53:10 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Django Classy Settings
======================

.. rubric:: Stay classy, Django.

Credits
-------

This work was originally inspired by the work of Jessie O'Connor.

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
   api
   changelog

Quickstart
----------

Install the package:

.. code-block:: bash

   $ pip install django-classy-settings

In your default ``settings.py``, add a `BaseSettings` class:

.. code-block:: python

    import cbs

    class BaseSettings():
        DEBUG = True

Derive testing/staging/production settings:

.. code-block:: python

    class LocalSettings(BaseSettings):
        ...

    class StagingSettings(BaseSettings):
        STATIC_ROOT = '....'

    class ProductionSettings(StagingSettings):
        DEBUG = False

Define on these classes settings that you want to change based on selection.
Any properties that look like settings (where name.is_uppper() is True) will be
included in your settings.  Any methods which match this will be called to
yield their values.

Finally, at the end of your ``settings.py``, apply the setting you want:

.. code-block:: python

    import os
    MODE = os.environ.get('DJANGO_MODE', 'Local')
    cbs.apply('{}Settings'.format(MODE.title()), globals())

All globaly declared settings will continue to work as expected, unless the
same name exists on the applied settings class.


Helpers
-------

We all like moving settings into the ENV, right?  So, here's a helper.

.. code-block:: python

    class Settings:

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


Also, you can pass a callable to cast the string to whatever you need, as well
as affect validation. Built in are ``as_bool``, ``as_list``, and ``as_tuple``
to intelligently cast values to bools, lists, and tuples.

.. code-block:: python

   class BaseSettings(cbs.BaseSettings):

       @cbs.env(cast=int)
       def COUNT_LIMIT(self):
           return 6

As an additional helper, there is ``cbs.envbool`` which subclasses ``cbs.env``
and sets `cast` to ``as_bool``.

``as_bool`` will strip white spaces and lower-case the given value, testing
it against two lists:

True::

    'y', 'yes', 'on', 't', 'true', '1'

False::

    'n', 'no', 'off', 'f', 'false', '0'

Any other value will raise a ValueError.

The ``as_list`` and ``as_tuple`` converters will take the input string and
split it at ``,``. Additionally, these functions will strip leading and
trailing white spaces from each item.

Finally, you can define an env setting that _must_ have an env var set, and has
no default.

.. code-block:: python

   class BaseSettings(object):
        REQUIRED = cbs.env(None, key='REQUIRED')

.. note:: You _must_ define ``key``, as there is no way otherwise for the
    descriptor to know its name.

This will raise a `RuntimeError` if the key `REQUIRED` is not set in the
environ.

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

Global Defaults
---------------

Previously this package provided ``GlobalSettings`` as a base class to give you
access to the default Django settings values.

This approach has been deprecated. Instead, to access Django's default settings
use:

.. code-block:: python

   from django.conf import global_settings as default

You can now reference default settings as follows:

.. code-block:: python

   MIDDLEWARE = default.MIDDLEWARE + [....]


Complex Values
--------------

A common question is how to handle complex settings, like DATABASES.


.. code-block:: python

   class BaseSettings:
       @cbs.env
       def DB_NAME(self):
          return 'test-db'

       @cbs.env
       def DB_USER(self):
          return 'test-user'

       @property
       def DATABASES(self):
           return {
               'default': {
                   'NAME': self.DB_NAME,
                   'USER': self.DB_USER,
                   ...
               }
           }

This way, sub-classes can set DB_NAME and so on, or they can be overidden by
environment variables.
