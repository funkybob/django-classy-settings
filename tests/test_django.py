from unittest import TestCase

from django.conf import Settings


class DjangoTestCase(TestCase):
    def test_settings(self):

        with self.assertRaises(ValueError):
            Settings("tests.settings")
