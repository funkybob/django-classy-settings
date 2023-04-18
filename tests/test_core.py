import importlib
import os
import unittest

from . import settings  # So reload works first time


class TestPython(unittest.TestCase):

    def test_precedence(self):
        os.environ["DJANGO_MODE"] = "global"

        importlib.reload(settings)

        self.assertEqual(settings.GLOBAL, "global")
