Tips and Best Practices
=======================

Here's some things to keep in mind.

Common Parts
------------

Continuing from the use of BASE_DIR in stock settings, you can make your
settings easier to manage by including common base parts that sub-classes can
alter.

.. code-block:: python

    class StagingSettings(BaseSettings):
        DOCROOT = '/path/to/web/server/docroot/'

        @property
        def STATIC_ROOT(self):
            return os.path.join(self.DOCROOT, 'static/')


    class ProductionSettings(StagingSettings):

        DOCTOOR = '/path/to/different/docroot/'


Cache expensive properties
--------------------------

If you have a setting that is calculated and is accessed frequently, you can
speed it up by using Django's ``cached_property`` decorator.  This will ensure
the value is only calculated once, then stored on the settings instance where
Python will find it in future.

.. code-block:: python

    from django.utils.functional import cached_property


    class BaseSettings(cbs.BaseSettings):

        @cached_property
        def DATABASES(self):
            import json

            with open('database.json', 'rb') as fin:
                return json.load(fin)

Remember that sometimes, even if a value is quick to calculate, if it's accessed
frequently it can be worthwhile caching it.

Composition over Inheritance
----------------------------

You can make your settings tidier by maintaining separate mixin classes for
each app.

You can even have a Debug/Staging/Production variant of each, and mix in the
right one for your settings mode.

