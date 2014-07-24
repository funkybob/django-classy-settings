
Simple Example
==============

Make a settings directory, and into __init__.py put:

.. code-block:: python

    import os

    import cbs


    class BaseSettings(cbs.BaseSettings):
        PROJECT_NAME = 'myproject'

        # ... your general default settings ...


    class LocalSettings(BaseSettings):
        # Settings for local development


    class StagingSettings(BaseSettings):
        # ...

        DOCROOT = '/path/to/docroot/'

        @property
        def STATIC_ROOT(self):
            return os.path.join(self.DOCROOT, 'static', '')

        @property
        def MEDIA_ROOT(self):
            return os.path.join(self.DOCROOT, 'media', '')


    class ProductionSettings(StagingSettings):
        DEBUG = False


    MODE = os.environ.get('DJANGO_MODE', 'Local')
    cbs.activate('{}Settings'.format(MODE.title()))

Now, you can set DJANGO_MODE in your environment to the settings you want to run.

.. code-block:: sh

    DJANGO_MODE=staging ./manage.py runserver

