from unittest import TestCase

from django.conf import Settings


class DjangoTestCase(TestCase):
    def test_settings(self):
        Settings("tests.settings")
