import importlib
import os
import unittest

from . import settings  # So reload works first time


class TestPython(unittest.TestCase):

    def test_precedence(self):
        os.environ["DJANGO_MODE"] = "global"

        importlib.reload(settings)

        self.assertEqual(settings.GLOBAL, "global")

    def test_non_upper(self):
        '''We only allow access to SHOUTY_SNAKE_CASE names.'''
        with self.assertRaises(AttributeError):
            settings.private

    def test_nested(self):
        '''
        Ensure when we access nested SHOUTY_SNAKE_CASE we still treat methods as properties.
        '''
        self.assertEqual(settings.METHOD, settings.NESTED)
