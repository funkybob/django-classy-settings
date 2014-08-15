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

        DOCROOT = '/path/to/different/docroot/'


Composition over Inheritance
----------------------------

You can make your settings tidier by maintaining separate mixin classes for
each app.

You can even have a Debug/Staging/Production variant of each, and mix in the
right one for your settings mode.

