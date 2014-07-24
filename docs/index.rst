.. Django Classy Settings documentation master file, created by
   sphinx-quickstart on Thu Jul 24 13:53:10 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Django Classy Settings's documentation!
==================================================

Overview
--------

Class-based settings make it easy for you to manage multiple settings for your
Django project, without ever copying values.

Interdependant values, values sourced from the env, even calculated values are
no problem, since you have the full power of Python and its classes.

Quickstart
----------

Make a settings module:

.. code-block:: sh

    mkdir settings

Create your core settings:

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

Finally, activate the setting you want:

.. code-block:: python

    # By class
    cbs.activate(LocalSettings)

    # By name
    cbs.activate('StagingSettings')

    # By import
    cbs.activate('myproj.settings.staging.StagingSettings')


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
