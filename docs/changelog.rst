Change Log
==========

3.0.6 (2024-??-??)
------------------

Features Added:

- Added `BaseSettings.Unset` to allow a class to un-set an inherited setting.
  This is useful to allow overriding Django defaults in development, and
  reverting in other configurations.

- An `env` can now be explicitly marked as mandatory by using `NAME = env(env.Required)`

- `use()` will now `warn` when any setting on a `BaseSetting` is masked by a
  setting defined outside a settings class.
  Because of the rules of `__getattr__` these Class Settings would never be used.

3.0.5 (2024-03-15)
------------------

Features Added:

- All accesses to SHOUTY_SNAKE_CASE methods on a `BaseSettings` class will now
  be treated as properties.
  Previously accessing these from within a method would require remembering to
  call it.

3.0.4 (2023-11-16)
------------------

Features Added:

- Guarantee a `Settings` class is only instantiated once per call to `use()`
  Note: `getattr_factory` and `dir_factory` are no longer classmethods.
- Break out `get_settings_instance` method from `use` for more flexibility.
- Add more helpful error message when a sub-class can't be found.

Cleanup:

- Moved `BaseSettings` out of `__init__` into its own file.

3.0.3 (2023-06-28)
------------------

Features Added:

- Raise exception when `env()` is called without any arguments at all.

3.0.2 (2023-04-20)
------------------

Housekeeping:

- Added Django 4.2 to CI
- Added Python 3.11 to CI
- Dropped Django 2.2 from CI
- Documentation corrections and clarifications

Features Added:

- `__dir__` now calculates visible attributes every call, instead of when it's constructed.
- `env` instances are now callable, making them somewhat usable outside of classes

3.0.1 (2022-09-15)
------------------

.. warning:: The previous release does not work with Django.

   This release is to fix that glaring mistake.

Bugs Fixed:

- Changed to using lookup syntax to creat prefixed env classes
- Added __dir__ as second return value from `use()` to satisfy Django settings

3.0.0 (2022-09-08)
------------------


.. admonition:: Backwards incompatible changes!

   This release makes major API changes and drops support for some features.

Major overhaul of the code base.

- Supports Python 3.7+
- Removed `toggle` feature entirely.

Features Added:

- Pre-canned typed `env` helpers: `env.bool`, `env.int`, `env.dburl`,
  `env.list`, `env.tuple`
- `BaseSettings` class, with `getattr_factory` and auto-subclass resolution.

2.1.1 (2017-09-22)
------------------

- Renamed @env(type) to cast

Bugs Fixed:

- Fix required env vars not having a name to look up (Thanks pgcd!)

2.1.0 (2017-08-10)
------------------

Removed:

- Dropped Python2 support.
- Removed deprecated ``cbs.BaseSettings``

2.0.1 (2016-04-16)
------------------

Features Added:

- You can now have an env var that _must_ have an env set.
- New `as_list` and `as_tuple` utility functions for casting values
  [Thanks MarkusH]

2.0.0 (2016-02-08)
------------------

The 'softer-touch' branch.

As of 2.0, `django-classy-settings` is advocating a "minimal impact" approach.

As such, it's recommended you retain the default ``settings.py`` as provided by
Django, and only move to a class those settings which change based on
environment.

Deprecation:

- Remove ``cbs.base``
- No longer import ``BaseSettings`` in ``cbs``
- Purged ``cbs.base``
- Moved ``cbs.base.GlobalSettings`` into ``cbs``

1.1.8 (2015-12-??)
------------------

Features Added:

- Use `inspect.ismethod` instead of just `callable` for detecting methods on
  settings classes.

Deprecation:

- Removed ill concieved `@cbs.returns_callable`.  Document a solution instead.

1.1.7 (2015-12-02)
------------------

Features Added:

- Added `@cbs.returns_callable` for settings that return callables

1.1.6 (2015-11-29)
------------------

Features Added:

- Tox config was overhauled, and hooked into "setup.py test" (Thanks TC)

Bugs Fixed:

- Fix case where @env(...) would return a partial on env, instead of the
  sub-class, which broke envbool (Thanks TC)

1.1.5 (2015-11-05)
------------------

Features Added:

- Added Django 1.9 base settings

1.1.4 (2015-09-25)
------------------

Features Added:

- Added Travis CI and tox config files
- Match Django for detecting settings
- Added GlobalSettings mixin

Bugs Fixed:

- Only apply type cast in @env to values sourced from environment.
- Correct call to setdefault in envbool

1.1.3 (2015-08-19)
------------------

Bugs Fixed:

- Moved TEMPLATE_DEBUG setting to Django 1.6/1.7 settings, as it's no longer
  valid in Django 1.8.

1.1.2 (2015-07-22)
------------------

Bugs Fixed:

- Type-cast values before caching

1.1.1 (2015-07-04)
------------------

Features Added:

+ Added tests (Thanks David Sanders)

Bugs Fixed:

- Fixed bug where we passed the env class instead of the settings object to the
  default method.

1.1.0 (2015-03-31)
------------------

Features Added:

+ Added type casting to @cbs.env
+ Added Django 1.8 default settings
+ Move settings into separate modules
+ Added Feature Toggle tool.

1.0.3 (2015-02-18)
------------------

Features Added:

+ Added cbs.boolenv

1.0.2 (2015-02-05)
------------------

Features Added:

+ Support different BaseSettings for different Django versions
+ Use Django's bundled version of six
+ Raise a ValueError if we can't find the settings class

Bugs fixed:

+ Fixed packaging for requirements

1.0.1 (2014-08-15)
------------------

Features Added:

+ Added DEFAULT_ENV_PREFIX


1.0.0 (2014-08-12)
------------------

Initial Release
