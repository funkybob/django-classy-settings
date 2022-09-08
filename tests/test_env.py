import os
import unittest

import cbs
from cbs import env


class EnvTestCase(unittest.TestCase):

    def setUp(self):
        '''
        Clear the env dict before each test.
        '''
        os.environ.clear()
        cbs.DEFAULT_ENV_PREFIX = ''


class TestEnv(EnvTestCase):

    def test_retrieve_from_method(self):
        class Settings:
            @env
            def SETTING(self):
                return 'bar'

        self.assertEqual(Settings().SETTING, 'bar')

    def test_retrieve_from_env(self):
        class Settings:
            @env
            def SETTING(self):
                raise ValueError()  # pragma: no cover

        os.environ['SETTING'] = 'foo'
        self.assertEqual(Settings().SETTING, 'foo')

    def test_retrieve_from_env_specifying_key(self):
        class Settings:
            @env(key='DJANGO_SETTING')
            def SETTING(self):
                raise ValueError()  # pragma: no cover

        os.environ['DJANGO_SETTING'] = 'foo'
        self.assertEqual(Settings().SETTING, 'foo')

    def test_retrieve_from_env_specifying_prefix(self):
        class Settings:
            @env(prefix='DJANGO_')
            def SETTING(self):
                raise ValueError()  # pragma: no cover

        os.environ['DJANGO_SETTING'] = 'foo'
        self.assertEqual(Settings().SETTING, 'foo')

    def test_default_env_prefix(self):
        cbs.DEFAULT_ENV_PREFIX = 'DJANGO_'

        class Settings:
            @env
            def SETTING(self):
                raise ValueError()  # pragma: no cover

        os.environ['DJANGO_SETTING'] = 'foo'
        self.assertEqual(Settings().SETTING, 'foo')

    def test_refer_to_other_setting(self):

        class Settings:
            OTHER = True

            @env
            def SETTING(self):
                return self.OTHER

        self.assertEqual(Settings().SETTING, True)


class EnvBoolTest(EnvTestCase):

    def test_env_bool_default(self):
        class Settings:

            @env.bool
            def SETTING(self):
                return None

        s = Settings()

        self.assertEqual(s.SETTING, None)

    def test_immediate(self):

        class Settings:

            DEBUG = env.bool(False)


        s = Settings()

        self.assertFalse(s.DEBUG)

        os.environ['DEBUG'] = 'y'
        del s.DEBUG
        self.assertTrue(s.DEBUG)


    def test_env_bool_casting(self):

        class Settings:
            @env.bool
            def SETTING(self):
                return None

        s = Settings()

        # Verify default, and prime cache
        self.assertIsNone(s.SETTING)

        # True values
        for tval in ('y', 'yes', 'on', 't', 'true', '1'):
            os.environ['SETTING'] = tval
            del s.SETTING
            self.assertTrue(s.SETTING)

            os.environ['SETTING'] = tval.title()
            del s.SETTING
            self.assertTrue(s.SETTING)

            os.environ['SETTING'] = tval.upper()
            del s.SETTING
            self.assertTrue(s.SETTING)

        for fval in ('n', 'no', 'off', 'f', 'false', '0'):
            os.environ['SETTING'] = fval
            del s.SETTING
            self.assertFalse(s.SETTING)

            os.environ['SETTING'] = fval.title()
            del s.SETTING
            self.assertFalse(s.SETTING)

            os.environ['SETTING'] = fval.upper()
            del s.SETTING
            self.assertFalse(s.SETTING)

    def test_env_bool_set_invalid(self):

        class Settings:

            @env.bool
            def SETTING(self):
                raise ValueError()  # pragma: no cover

        s = Settings()

        for value in [
            'yep', 'nah', '-1', '10', '00', '', 'Y Y',
        ]:
            os.environ['SETTING'] = value
            # Since it raises an exception, we don't have to clear the cache
            with self.assertRaises(ValueError):
                s.SETTING
