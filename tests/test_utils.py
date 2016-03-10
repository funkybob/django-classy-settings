import unittest

from cbs.utils import as_bool, as_list, as_tuple


class UtilsEnv(unittest.TestCase):

    def test_as_bool(self):
        yes = ('Y', 'yes', 'ON', 't', 'TrUe', '1', True)
        no = ('N', 'no', 'OFF', 'f', 'FaLsE', '0', False)
        for value in yes:
            self.assertTrue(as_bool(value))
        for value in no:
            self.assertFalse(as_bool(value))
        self.assertRaisesRegexp(
            ValueError,
            "Unrecognised value for bool: 'blub blah'",
            as_bool,
            'blub blah'
        )

    def test_as_list(self):
        values = (
            (['foo'], ['foo']),
            ('', []),
            ('foo', ['foo']),
            ('foo,bar', ['foo', 'bar']),
            ('FOO,  bar  ,  buz', ['FOO', 'bar', 'buz']),
            ('example.com,www.example.com,other.com', ['example.com', 'www.example.com', 'other.com']),
        )
        for given, expected in values:
            self.assertEqual(as_list(given), expected)

    def test_as_tuple(self):
        values = (
            (('foo',), ('foo',)),
            ('', ()),
            ('foo', ('foo',)),
            ('foo,bar', ('foo', 'bar')),
            ('FOO,  bar  ,  buz', ('FOO', 'bar', 'buz')),
            ('example.com,www.example.com,other.com', ('example.com', 'www.example.com', 'other.com')),
        )
        for given, expected in values:
            self.assertEqual(as_tuple(given), expected)
