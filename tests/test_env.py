import os
import unittest

import cbs
from cbs import env


class EnvTestCase(unittest.TestCase):
    def setUp(self):
        """
        Clear the env dict before each test.
        """
        os.environ.clear()


class TestPartial(EnvTestCase):

    def test_prefix(self):

        denv = env['DJANGO_']

        class Settings:
            SETTING = denv('value')
            BOOL = denv.bool(True)

        os.environ['DJANGO_SETTING'] = 'override'
        self.assertEqual(Settings().SETTING, 'override')


class TestImmediate(EnvTestCase):
    def test_default(self):
        class Settings:
            SETTING = env("value")

        self.assertEqual(Settings().SETTING, "value")

    def test_override(self):
        class Settings:
            SETTING = env("value")

        os.environ["SETTING"] = "override"
        self.assertEqual(Settings().SETTING, "override")

    def test_with_key(self):
        class Settings:
            SETTING = env("value", key="OTHER")

        os.environ["OTHER"] = "override"
        self.assertEqual(Settings().SETTING, "override")

    def test_with_prefix(self):
        class Settings:
            SETTING = env("value", prefix="PREFIX_")

        os.environ["PREFIX_SETTING"] = "override"
        self.assertEqual(Settings().SETTING, "override")

    def test_with_prefix_and_key(self):
        class Settings:
            SETTING = env("value", key="OTHER", prefix="PREFIX_")

        os.environ["PREFIX_OTHER"] = "override"
        self.assertEqual(Settings().SETTING, "override")


class TestMethod(EnvTestCase):
    def test_default(self):
        class Settings:
            @env
            def SETTING(self):
                return "value"

        self.assertEqual(Settings().SETTING, "value")

    def test_override(self):
        class Settings:
            @env
            def SETTING(self):
                raise ValueError()  # pragma: no cover

        os.environ["SETTING"] = "override"
        self.assertEqual(Settings().SETTING, "override")

    def test_with_key(self):
        class Settings:
            @env(key="OTHER")
            def SETTING(self):
                raise ValueError()  # pragma: no cover

        os.environ["OTHER"] = "override"
        self.assertEqual(Settings().SETTING, "override")

    def test_with_prefix(self):
        class Settings:
            @env(prefix="PREFIX_")
            def SETTING(self):
                raise ValueError()  # pragma: no cover

        os.environ["PREFIX_SETTING"] = "override"
        self.assertEqual(Settings().SETTING, "override")

    def test_with_prefix_and_key(self):
        class Settings:
            @env(key="OTHER", prefix="PREFIX_")
            def SETTING(self):
                raise ValueError()  # pragma: no cover

        os.environ["PREFIX_OTHER"] = "override"
        self.assertEqual(Settings().SETTING, "override")

    def test_refer_to_other_setting(self):
        class Settings:
            OTHER = True

            @env
            def SETTING(self):
                return self.OTHER

        self.assertEqual(Settings().SETTING, True)


class EnvBoolTest(EnvTestCase):
    def test_immediate(self):
        class Settings:

            DEBUG = env.bool(False)

        os.environ["DEBUG"] = "y"
        self.assertTrue(Settings().DEBUG)

    def test_default(self):
        class Settings:
            @env.bool
            def SETTING(self):
                return None

        self.assertEqual(Settings().SETTING, None)

    def test_env_bool_casting(self):
        class Settings:
            @env.bool
            def SETTING(self):
                return None

        s = Settings()

        # Verify default, and prime cache
        self.assertIsNone(s.SETTING)

        # True values
        for tval in ("y", "yes", "on", "t", "true", "1"):
            os.environ["SETTING"] = tval
            del s.SETTING
            self.assertTrue(s.SETTING)

            os.environ["SETTING"] = tval.title()
            del s.SETTING
            self.assertTrue(s.SETTING)

            os.environ["SETTING"] = tval.upper()
            del s.SETTING
            self.assertTrue(s.SETTING)

        for fval in ("n", "no", "off", "f", "false", "0"):
            os.environ["SETTING"] = fval
            del s.SETTING
            self.assertFalse(s.SETTING)

            os.environ["SETTING"] = fval.title()
            del s.SETTING
            self.assertFalse(s.SETTING)

            os.environ["SETTING"] = fval.upper()
            del s.SETTING
            self.assertFalse(s.SETTING)

    def test_env_bool_set_invalid(self):
        class Settings:
            @env.bool
            def SETTING(self):
                raise ValueError()  # pragma: no cover

        s = Settings()

        for value in [
            "yep",
            "nah",
            "-1",
            "10",
            "00",
            "",
            "Y Y",
        ]:
            os.environ["SETTING"] = value
            # Since it raises an exception, we don't have to clear the cache
            with self.assertRaises(ValueError):
                s.SETTING


class EnvIntTest(EnvTestCase):
    def test_immediate(self):
        class Settings:
            SETTING = env.int("5432")

        self.assertEqual(Settings().SETTING, 5432)

    def test_override(self):
        class Settings:
            SETTING = env.int("5432")

        os.environ["SETTING"] = "2345"
        self.assertEqual(Settings().SETTING, 2345)


class EndDbUrlTest(EnvTestCase):
    def test_default(self):
        class Settings:
            SETTING = env.dburl("postgres://hostname/dbname")

        value = Settings().SETTING

        self.assertEqual(
            value,
            {
                "ENGINE": "django.db.backends.postgresql",
                "HOST": "hostname",
                "NAME": "dbname",
            },
        )

    def test_override(self):
        class Settings:
            SETTING = env.dburl("default")

        os.environ["SETTING"] = "postgres://hostname/dbname"
        value = Settings().SETTING

        self.assertEqual(
            value,
            {
                "ENGINE": "django.db.backends.postgresql",
                "HOST": "hostname",
                "NAME": "dbname",
            },
        )


class EnvListTest(EnvTestCase):
    def test_immediate(self):
        class Settings:
            SETTING = env.list(["foo", "bar"])

        self.assertEqual(Settings().SETTING, ["foo", "bar"])

    def test_override(self):
        class Settings:
            SETTING = env.list([1])

        os.environ["SETTING"] = "one, two"

        self.assertEqual(Settings().SETTING, ["one", "two"])


class EnvTupleTest(EnvTestCase):
    def test_immediate(self):
        class Settings:
            SETTING = env.tuple(
                (
                    "foo",
                    "bar",
                )
            )

        self.assertEqual(
            Settings().SETTING,
            (
                "foo",
                "bar",
            ),
        )

    def test_override(self):
        class Settings:
            SETTING = env.tuple((1,))

        os.environ["SETTING"] = "one, two"

        self.assertEqual(
            Settings().SETTING,
            (
                "one",
                "two",
            ),
        )
