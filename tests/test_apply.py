import unittest
import cbs


class AttrSettings():
    PROJECT_NAME = 'fancy_project'


class MethodSettings():
    def PROJECT_NAME(self):
        return 'fancy_project'


class TestApply(unittest.TestCase):

    def test_apply_settings_attr(self):
        g = {}
        cbs.apply(AttrSettings, g)

        self.assertEqual(g['PROJECT_NAME'], 'fancy_project')

    def test_apply_settings_method(self):
        g = {}
        cbs.apply(MethodSettings, g)

        self.assertEqual(g['PROJECT_NAME'], 'fancy_project')

    def test_apply_settings_string_local(self):
        g = {'AttrSettings': AttrSettings}
        cbs.apply('AttrSettings', g)

        self.assertEqual(g['PROJECT_NAME'], 'fancy_project')

    def test_apply_settings_string_reference(self):
        g = {}
        cbs.apply(__name__ + '.AttrSettings', g)

        self.assertEqual(g['PROJECT_NAME'], 'fancy_project')

    def test_apply_settings_invalid_string_local(self):
        self.assertRaises(ValueError, cbs.apply, 'LocalSettings', {})

    def test_apply_settings_invalid_string_reference(self):
        self.assertRaises(ImportError, cbs.apply, 'invalid.Class', {})
