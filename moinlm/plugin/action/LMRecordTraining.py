# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - Training Documentation Action

    This action sends a form allowing the user to invoke action
    LMWriteTrainingLog.py

    @copyright: 2008 Noah Hoffman <ngh2@uw.edu>
    @license: UW Free Fork
"""

from MoinMoin.Page import Page


def execute(pagename, request):

    msg = """
    <form method="post" action="">
    <input type="hidden" name="action" value="lmWriteTrainingLog">
    <input type="submit" name="button" value="I have read this page">
    </form>

    <ul>
    <li>This action is intended to document that this page has been
    read and understood.</li>
    <li>Please press this button to document that you have read this
    page or click "Clear message" below to cancel.</li>
    </ul>
    """

    request.theme.add_msg(msg)
    Page(request, pagename).send_page()
