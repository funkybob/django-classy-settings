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

Valid settings are any property or callable for which ``isupper()`` returns
`True`.
