===
API
===

---------
Functions
---------

@env
----

The env decorator simplifies defining a setting from an evironment variable.

It accepts two optional arguments:

key
   Overrides the environment variable name checked for this value.

prefix
   Prefixes the method name to determine the environment variable checked
   for this value.

type
   A callable to help with type-casting values.

The key is always prefixed, using the value of cbs.DEFAULT_ENV_PREFIX if none is specified.

apply
-----

.. code-block:: python

   def apply(source, target)

The `apply` function updates the target with the settings it gleans from
`source`.

If `source` is a string, it will be treated as an import path for the class to
introspect for settings.  Otherwise, it will be considered the object to
inspect.

Valid settings are any property or callable where the name matches itself when .upper() is applied.

-------------------
Scaffolding Classes
-------------------

CoreSettings
------------

A scaffolding class that contains common settings.

.. class:: CoreSettings()

   .. attribute:: BASE_DIR

      A property that resolves to the parent dir of the dir the settings class
      is defined in.

   .. attribute:: DEBUG = True

   .. attribute:: DEBUG_TEMPLATE

      A property that resolves to the value of self.DEBUG

   .. attribute:: ALLOWED_HOSTS = []

   .. attribute:: ROOT_URLCONF

      A property that resolves to '{}.urls' where {} is replaced with
      self.PROJECT_NAME

   .. attribute:: WSGI_APPLICATION

      A property that resolves to '{}.wsgi.application'

BaseSettings
------------

An alias for `Base16Settings` or `Base17Settings` depending on the current
Django version.

Base16Settings
--------------

Base settings for a Django 1.6 project.  For values, see the Django docs.

.. class:: Base16Settings(CoreSettings)

   .. attribute:: INSTALLED_APPS
   .. attribute:: MIDDLEWARE_CLASSES

   .. attribute:: DATABASES

   .. attribute:: LANGUAGE_CODE
   .. attribute:: TIME_ZONE
   .. attribute:: USE_I18N
   .. attribute:: USE_L10N
   .. attribute:: USE_TZ

   .. attribute:: STATIC_URL

Base17Settings
--------------

Base settings for a Django 1.7 project.  For values, see the Django docs.

.. class:: Base17Settings(CoreSettings)

   .. attribute:: INSTALLED_APPS
   .. attribute:: MIDDLEWARE_CLASSES

   .. attribute:: DATABASES

   .. attribute:: LANGUAGE_CODE
   .. attribute:: TIME_ZONE
   .. attribute:: USE_I18N
   .. attribute:: USE_L10N
   .. attribute:: USE_TZ

   .. attribute:: STATIC_URL

