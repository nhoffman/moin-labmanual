#!/usr/bin/env python

import sys
import os
import unittest
import logging
from collections import namedtuple
from operator import attrgetter

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
        self.assertRaises(ValueError, utils.parse_args, u'c=CCC', ['a', 'b'], b='BBB')


class TestPivot(unittest.TestCase):
    def test01(self):
        rows = [('Apple',      'Coles',      1.50),
        ('Apple',      'Woolworths', 1.60),
        ('Apple',      'IGA',        1.70),
        ('Banana',     'Coles',      0.50),
        ('Banana',     'Woolworths', 0.60),
        ('Banana',     'IGA',        0.70),
        ('Cherry',     'Coles',      5.00),
        ('Date',       'Coles',      2.00),
        ('Date',       'Woolworths', 2.10),
        ('Elderberry', 'IGA',        10.00)]

        Row = namedtuple('Row', ['fruit', 'store', 'price'])

        rows = [Row(*row) for row in rows]
        table = list(utils.pivot(
            rows, rowattr='fruit', colattr='store', cellfun=attrgetter('price'),
            nullval=None))

        # for row in table:
        #     print row

        # column names
        self.assertListEqual(table[0], [None] + sorted({row.store for row in rows}))

        # row names
        self.assertListEqual(
            [row[0] for row in table],
            [None] + sorted({row.fruit for row in rows}))


if __name__ == '__main__':
    unittest.main()
