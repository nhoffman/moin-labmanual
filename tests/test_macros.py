#!/usr/bin/env python

import re
import unittest
import logging

from MoinMoin.web.contexts import ScriptContext
from MoinMoin.Page import Page
from MoinMoin.logfile import editlog

from moinlm.plugin.macro.LMPageList2 import get_last_approved, get_page_status

log = logging

request = ScriptContext()


class TestLMReviewStatus(unittest.TestCase):
    def setUp(self):
        self.page = Page(request, u'LMDocumentExample')
        self.log = editlog.EditLog(request, rootpagename=self.page.page_name)

    def test01(self):
        filtered = get_last_approved(request, self.log)
        self.assertEqual(filtered.rev, '00000003')

    def test02(self):
        filtered = get_last_approved(
            request, self.log, log_re=re.compile('reviewed', re.IGNORECASE))
        self.assertEqual(filtered.rev, '00000002')

    def test03(self):
        status = get_page_status(self.page, request)
        self.assertEqual(status.rev, '3')

    def test04(self):
        status = get_page_status(
            self.page, request, log_rexp='reviewed')
        self.assertEqual(status.rev, '2 (3)')

    def test05(self):
        status = get_page_status(self.page, request, log_rexp='foo')
        self.assertFalse(status.ever_approved)


if __name__ == '__main__':
    unittest.main()
