import importlib
import os
import unittest

from . import settings  # So reload works first time


class TestSettingsUse(unittest.TestCase):
    def setUp(self):
        os.environ.clear()

    def test_use(self):
        importlib.reload(settings)

        self.assertEqual(settings.GLOBAL, "global")

        self.assertTrue(settings.DEBUG)
        self.assertEqual(settings.STR_ENV, "default")
        self.assertFalse(settings.BOOL_ENV)
        self.assertEqual(settings.METHOD, "True")

        self.assertEqual(settings.IMMEDIATE_INT, 5432)

        with self.assertRaises(ValueError):
            settings.STR_REQUIRED

    def test_use_prod(self):
        os.environ["DJANGO_MODE"] = "prod"
        os.environ["IMMEDIATE_INT"] = "2345"

        importlib.reload(settings)

        self.assertFalse(settings.DEBUG)
        self.assertEqual(settings.STR_ENV, "default")
        self.assertTrue(settings.BOOL_ENV)
        self.assertEqual(settings.METHOD, "False")

        self.assertEqual(settings.IMMEDIATE_INT, 2345)

    def test_use_env(self):
        os.environ["DJANGO_MODE"] = "prod"
        os.environ["STR_ENV"] = "override"
        os.environ["BOOL_ENV"] = "f"

        importlib.reload(settings)

        self.assertFalse(settings.DEBUG)
        self.assertEqual(settings.STR_ENV, "override")
        self.assertFalse(settings.BOOL_ENV)
        self.assertEqual(settings.METHOD, "False")

    def test_use_unknown(self):
        os.environ["DJANGO_MODE"] = "mystery"

        with self.assertRaises(
            ValueError,
            msg="Could not find Settings class for mode 'mystery' "
                "(Known: Settings, ProdSettings, GlobalSettings)",
        ):
            importlib.reload(settings)

    def test_unset(self):
        os.environ["DJANGO_MODE"] = "global"

        importlib.reload(settings)

        with self.assertRaises(AttributeError):
            settings.IMMEDIATE_INT

    def test_warning(self):
        os.environ["DJANGO_MODE"] = "global"

        with self.assertWarns(UserWarning):
            importlib.reload(settings)

