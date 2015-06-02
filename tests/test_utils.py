#!/usr/bin/env python

import sys
import os
import unittest
import logging

from moinlm import utils

log = logging


class TestParseArgs(unittest.TestCase):

    def test01(self):
        self.assertEqual(utils.parse_args(u''), {})
        self.assertEqual(utils.parse_args(u'AAA', ['a']), {'a': u'AAA'})
        self.assertEqual(utils.parse_args(u'a=AAA', ['a']), {'a': u'AAA'})
        self.assertEqual(utils.parse_args(u'', ['a', 'b']),
                         {'a': None, 'b': None})
        self.assertEqual(utils.parse_args(u'AAA', ['a', 'b']),
                         {'a': u'AAA', 'b': None})
        self.assertEqual(utils.parse_args(u'AAA,BBB', ['a', 'b']),
                         {'a': u'AAA', 'b': u'BBB'})
        self.assertEqual(utils.parse_args(u'AAA,b=BBB', ['a', 'b']),
                         {'a': u'AAA', 'b': u'BBB'})
        # provides a default value for 'b'
        self.assertEqual(utils.parse_args(u'AAA', ['a', 'b'], b='BBB'),
                         {'a': u'AAA', 'b': u'BBB'})

        # positionl argument provided when none are defined
        self.assertRaises(ValueError, utils.parse_args, u'AAA')


if __name__ == '__main__':
    unittest.main()
