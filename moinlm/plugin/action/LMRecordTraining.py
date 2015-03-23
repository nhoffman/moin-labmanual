# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - Training Documentation Action

    This action sends a form allowing the user to invoke action
    LMWriteTrainingLog.py

    @copyright: 2008 Noah Hoffman <ngh2@uw.edu>
    @license: UW Free Fork
"""

from MoinMoin.Page import Page
from MoinMoin.util import timefuncs

from moinlm.training import record_training


def execute(pagename, request):

    _ = request.getText
    page = Page(request, pagename)
    user = request.user

    if request.form.get('submitted_from_form', 'no') == 'yes':
        page_info = page.lastEditInfo()
        page_info['rev'] = repr(page.get_real_rev())
        page_info['user'] = user.name
        page_info['pagename'] = pagename
        page_info['timestamp'] = timefuncs.W3CDate()

        record_training(request, page_info)

        msg = """Thank you! You have documented that you have read
        revision %(rev)s of "%(pagename)s"
        """ % page_info

    else:
        msg = """
        <form method="post" action="">
        <input type="hidden" name="action" value="LMRecordTraining2">
        <input type="hidden" name="submitted_from_form" value="yes">
        <input type="submit" name="button" value="I have read this page">
        </form>

        <ul>
        <li>This action is intended to document that this page has been
        read and understood.</li>
        <li>Please press this button to document that you have read this
        page or click "Clear message" below to cancel.</li>
        </ul>
        """

    request.theme.add_msg(_(msg, formatted=False))
    page.send_page()
