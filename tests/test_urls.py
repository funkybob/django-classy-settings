from unittest import TestCase

from cbs.urls import parse_dburl


class TestUrlParse(TestCase):
    def test_simple(self):
        result = parse_dburl(
            "postgres://user:password@hostname:1234/dbname"
            "?conn_max_age=15&local_option=test"
        )

        self.assertEqual(
            result,
            {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": "dbname",
                "HOST": "hostname",
                "PORT": 1234,
                "PASSWORD": "password",
                "USER": "user",
                "CONN_MAX_AGE": 15,
                "OPTIONS": {
                    "local_option": "test",
                },
            },
        )

    def test_sqlite(self):
        result = parse_dburl("sqlite:///db.sqlite")

        self.assertEqual(
            result,
            {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": "db.sqlite",
            },
        )
