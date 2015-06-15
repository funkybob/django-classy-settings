import unittest
import cbs


class AttrSettings():
    PROJECT_NAME = 'fancy_project'


class MethodSettings():
    def PROJECT_NAME(self):
        return 'fancy_project'


class TestApply(unittest.TestCase):

    def test_apply_settings_attr(self):
        cbs.apply(AttrSettings, globals())

        self.assertEqual(PROJECT_NAME, 'fancy_project')

    def test_apply_settings_method(self):
        cbs.apply(MethodSettings, globals())

        self.assertEqual(PROJECT_NAME, 'fancy_project')

    def test_apply_settings_string_reference(self):
        cbs.apply(__name__ + '.AttrSettings', globals())

        self.assertEqual(PROJECT_NAME, 'fancy_project')

    def test_apply_settings_invalid_string_reference(self):
        self.assertRaises(ValueError, cbs.apply, 'invalid.Class', globals())
