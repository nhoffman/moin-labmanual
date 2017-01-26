# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - Training Documentation Action

    This action sends a form allowing the user to invoke action
    LMWriteTrainingLog.py
"""

from MoinMoin.Page import Page

from moinlm.training import record_training


def execute(pagename, request):

    _ = request.getText
    page = Page(request, pagename)

    if request.form.get('submitted_from_form') == 'yes':
        rev = repr(page.get_real_rev())
        record_training(request,
                        pagename=pagename,
                        rev=rev,
                        user=request.user.name)

        msg = """
        Thank you! You have documented that you have read revision {} of "{}"
        """.format(rev, pagename)
    else:
        msg = """
        <div>
        <form method="POST" action="">
        <input type="hidden" name="submitted_from_form" value="yes">
        <input type="submit" name="button" value="I have read this page">
        </form>

        <p>Please press the button above to document that you have read
        and understood this page or click "Clear message" below to
        cancel.</p>
        </div>
        """

    request.theme.add_msg(_(msg, formatted=False))
    page.send_page()
