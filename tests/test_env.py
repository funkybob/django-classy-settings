import os
import unittest
import cbs


class TestEnv(unittest.TestCase):

    def setUp(self):
        os.environ.clear()
        cbs.DEFAULT_ENV_PREFIX = ''

    def test_retrieve_from_method(self):
        class Settings:
            @cbs.env
            def SETTING(self):
                return 'bar'

        self.assertEqual(Settings().SETTING, 'bar')

    def test_retrieve_from_env(self):
        class Settings:
            @cbs.env
            def SETTING(self):
                return 'bar'

        os.environ['SETTING'] = 'foo'
        self.assertEqual(Settings().SETTING, 'foo')

    def test_retrieve_from_env_specifying_key(self):
        class Settings:
            @cbs.env(key='DJANGO_SETTING')
            def SETTING(self):
                return 'bar'

        os.environ['DJANGO_SETTING'] = 'foo'
        self.assertEqual(Settings().SETTING, 'foo')

    def test_retrieve_from_env_specifying_prefix(self):
        class Settings:
            @cbs.env(prefix='DJANGO_')
            def SETTING(self):
                return 'bar'

        os.environ['DJANGO_SETTING'] = 'foo'
        self.assertEqual(Settings().SETTING, 'foo')

    def test_default_env_prefix(self):
        cbs.DEFAULT_ENV_PREFIX = 'DJANGO_'

        class Settings:
            @cbs.env
            def SETTING(self):
                return 'bar'

        os.environ['DJANGO_SETTING'] = 'foo'
        self.assertEqual(Settings().SETTING, 'foo')

    def test_refer_to_other_setting(self):

        class Settings:
            OTHER = True

            @cbs.env
            def SETTING(self):
                return self.OTHER

        self.assertEqual(Settings().SETTING, True)

    def test_env_bool(self):
        class Settings:
            @cbs.envbool
            def SETTING(self):
                return None

        s = Settings()
        self.assertTrue(s.SETTING is None)

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

        os.environ['SETTING'] = 'nyet'
        del s.SETTING
        with self.assertRaises(ValueError):
            s.SETTING

    def test_envbool_default(self):

        class Settings:

            @cbs.envbool
            def SETTING(self):
                return True

        self.assertEqual(Settings().SETTING, True)

    def test_envbool_set_true(self):

        class Settings:

            @cbs.envbool
            def SETTING(self):
                return False

        for value in [
            'y', 'yes', 'on', 't', 'true', '1',
            'Y', 'YES', 'ON', 'T', 'TRUE',
            'Y ', ' YES', '  ON', '\tT', '\nTRUE',
            'yEs', 'On', 'True',
        ]:
            os.environ['SETTING'] = value
            self.assertEqual(Settings().SETTING, True)

    def test_envbool_set_false(self):

        class Settings:

            @cbs.envbool
            def SETTING(self):
                return True

        for value in [
            'n', 'no', 'off', 'f', 'false', '0',
            'N', 'NO', 'OFF', 'F', 'FALSE',
            ' N ', 'NO ', ' OFF', 'F\t', 'FALSE\n',
            'No', 'Off', 'fALSE',
        ]:
            os.environ['SETTING'] = value
            self.assertEqual(Settings().SETTING, False)

    def test_envbool_set_invalid(self):

        class Settings:

            @cbs.envbool
            def SETTING(self):
                return True

        for value in [
            'yep', 'nah', '-1', '10', '00', '', 'Y Y',
        ]:
            os.environ['SETTING'] = value
            self.assertRaises(ValueError, lambda: Settings().SETTING)

    def test_envbool_with_specified_key_set_true(self):

        class Settings:

            @cbs.envbool(key='MY_SETTING')
            def SETTING(self):
                return False

        os.environ['MY_SETTING'] = 'true'
        self.assertEqual(Settings().SETTING, True)

    def test_required_env(self):

        class Settings:

            SETTING = cbs.envbool(None, key='MY_SETTING')

        with self.assertRaises(RuntimeError):
            Settings().SETTING
