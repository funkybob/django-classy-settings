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
no problem, since you have the full power of Python and class inheritance.


Contents
--------

.. toctree::
   :maxdepth: 1

   api
   changelog

Quick Start
-----------

In your `settings.py`, after your existing settings, define a settings class:

.. code-block:: python

    from cbs import BaseSettings

    class Settings(BaseSettings):
        ...


For any settings you want to be overridable from environment variable, move them
to the `Settings` class:

.. code-block:: python

    from cbs import BaseSettings, env


    class Settings(BaseSettings):

        DEBUG = env.bool(True)

        STATIC_ROOT = env(None)

        DEFAULT_DATABASE = env.dburl('sqlite://db.sqlite')

        def DATABASES(self):
            return {
                'default': self.DEFAULT_DATABASE,
            }


Define per-target settings:

.. code-block:: python

    class TestSettings(Settings):
        DEBUG = False

Hook it into your settings:

.. code-block:: python

    __getattr__ = BaseSettings.use()

Now when you start Django, it will use all of your global settings, and any from ``Settings``.

You can switch to using the ``TestSettings`` by setting the `DJANGO_MODE` environment variable:

.. code-block:: bash

    $ DJANGO_MODE=test ./manage.py shell

`BaseSettings`
--------------

The `BaseSettings` class performs two roles:

#. Provides a factory for a module-level ``__getattr__`` function.

   This allows the class to transparently hook into your `settings.py`

#. Provides the ``user`` classmethod.

   This will take the value of the environment variable `DJANGO_MODE` and use it
   to find any sub-class of ``BaseSettings`` with that name, returning a
   ``__getattr__`` method using it.


The `env` property
------------------

To help with environment driven settings there is the `env` property decorator.

The simplest use case is with an immediate value:

.. code-block:: python

    class Settings(BaseSettings):

        FOO = env('default')

    __getattr__ = BaseSettings.use()


In this case, if the `FOO` environment variable is set, then ``settings.FOO``
will yield its value.  Otherwise, it will be ``"default"``.

You can optionally override the environment variable name to look up by passing a ``key`` argument:

.. code-block:: python

    class Settings(BaseSettings):

        FOO = env('default', key='BAR')

Additionally, you can define a prefix for the environment variable:

.. code-block:: python

    class Settings(BaseSettings):

        FOO = env('default', prefix='MY_')  # looks up env var MY_FOO

If you need a type other than ``str``, you can pass a ``cast`` callable, which will be passed the value.

.. code-block:: python

    class Settings(BaseSettings):

        FOO = env('default', cast=int)


For convenience, there are several built-in pre-defined cast types, accessible via the ``env`` decorator.

.. code-block:: python

    env.bool    # Treats ("y", "yes", "on", "t", "true", "1") as True, and ("n", "no", "off", "f", "false", "0") as False
    env.int     # Use the int constructor
    env.dburl   # Converts URLs to Django DATABASES entries.
    env.list    # splits on ',', and strips each value
    env.tuple   # as above, but yiels a tuple

In all cases, if the default value passed is a string, it will be passed to the cast function.

As a decorator
==============

Additionally, ``env`` will function as a decorator. This allows you to put some
logic into deciding the default value.

.. code-block:: python

    class Settings(BaseSettings):
        DEBUG = True

        @env.int
        def FOO(self):
            return 1 if self.DEBUG else 2


Mandatory environment variable
==============================

Should you require a value to *always* be supplied by environment variable, have your method raise a ``ValueError``


.. code-block:: python

    class Settings(BaseSettings):
        @env.int
        def REQUIRED(self):
            raise ValueError()


Avoiding repeated prefixes
==========================

To avoid having to specify a prefix on multiple related variables, ``env`` will yield a ``partial`` when no default is provided.

Let's say, for instance, you want all of your environment variables prefixed with `DJANGO_`

.. code-block:: python

    # Common prefix for REDIS related settings
    denv = env(prefix='DJANGO_')

    class Settings(BaseSettings):

        DEBUG = env(True)


Now setting ``DJANGO_DEBUG=f`` will disable debug mode.
