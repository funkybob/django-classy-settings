import unittest

from django.conf import global_settings as default

import cbs


class MySettings:

    @property
    def INSTALLED_APPS(self):
        # Customize an empty global setting.
        return list(default.INSTALLED_APPS) + ['test']

    @property
    def CACHES(self):
        # Customize a non-empty global setting.
        caches = default.CACHES
        caches['custom'] = {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}
        return caches


class GlobalSettingsTest(unittest.TestCase):

    def test_precedence_empty_global_setting(self):
        g = {}
        cbs.apply(MySettings, g)

        self.assertEqual(['test'], g['INSTALLED_APPS'])

    def test_precedence_non_empty_global_setting(self):
        g = {}
        cbs.apply(MySettings, g)

        self.assertIn('default', g['CACHES'])
        self.assertIn('custom', g['CACHES'])
