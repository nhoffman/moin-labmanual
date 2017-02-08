#!/usr/bin/env python

import sys
import os
import unittest
import logging
from collections import namedtuple
from operator import attrgetter

from MoinMoin.web.contexts import ScriptContext
from MoinMoin.Page import Page
from MoinMoin.logfile import editlog

from moinlm import utils
from moinlm.plugin.macro.LMPageList2 import filter_log

log = logging

request = ScriptContext()


class TestLMReviewStatus(unittest.TestCase):
    def setUp(self):
        page = Page(request, u'LMDocumentExample')
        self.log = editlog.EditLog(request, rootpagename=page.page_name)

    def test01(self):
        filtered = filter_log(request, self.log)
        self.assertEqual(filtered.rev, '00000003')

    def test02(self):
        filtered = filter_log(request, self.log, log_rexp='reviewed')
        self.assertEqual(filtered.rev, '00000002')



if __name__ == '__main__':
    unittest.main()
