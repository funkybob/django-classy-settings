
import unittest
import cbs


class MySettings(cbs.BaseSettings, cbs.GlobalSettings):
    PROJECT_NAME = 'tests'

    @property
    def TEMPLATE_LOADERS(self):
        return super(MySettings, self).TEMPLATE_LOADERS + ('test',)


class GlobalSettingsTest(unittest.TestCase):

    def test_precedence(self):
        cbs.apply(MySettings, globals())

        self.assertTrue(len(TEMPLATE_LOADERS), 3) 
