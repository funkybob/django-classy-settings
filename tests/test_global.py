
import unittest
import cbs


class MySettings(cbs.GlobalSettings):
    PROJECT_NAME = 'tests'

    @property
    def INSTALLED_APPS(self):
        return super(MySettings, self).INSTALLED_APPS + ('test',)


class GlobalSettingsTest(unittest.TestCase):

    def test_precedence(self):
        g = {}
        cbs.apply(MySettings, g)

        self.assertEqual(len(g['INSTALLED_APPS']), 1)
