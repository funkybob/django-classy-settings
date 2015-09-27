Change Log
==========

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
