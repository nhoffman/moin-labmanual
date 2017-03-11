# -*- coding: iso-8859-1 -*-
"""This action sends a form for deprecating the current page.

"""

import time
from MoinMoin.Page import Page
from MoinMoin.PageEditor import PageEditor

from moinlm.utils import is_deprecated


def execute(pagename, request):

    _ = request.getText
    page = Page(request, pagename)

    if is_deprecated(page):
        msg = 'This page is already marked as archived.'
    elif request.form.get('submitted_from_form') == 'yes':
        pg = PageEditor(request, pagename)
        rev = request.rev or 0
        user = request.user.name
        comment = ('ARCHIVED ' + request.form.get('comment', '')).strip()

        # save original page content with a comment
        savetext = '#deprecated\n'
        savetext += '## page archived by %s %s\n' % (user, time.asctime())
        savetext += page.get_raw_body().rstrip()

        try:
            pg.saveText(savetext, rev, trivial=False, comment=comment)
        except Exception, msg:
            pass
        else:
            msg = '{}" has been archived with the comment "{}"'.format(
                pagename, comment)
    else:
        msg = """
        <div>
        <p>
        Confirm that this page should be archived, or use the link below to cancel.
        </p>
        <form method="POST" action="">
        <input type="hidden" name="submitted_from_form" value="yes">
        <input type="submit" name="button" value="Archive">
        <input type="text" name="comment" value="" size="80" maxlength="80"
         placeholder="(optional comment)">
        </form>
        </div>
        """

    request.theme.add_msg(_(msg, formatted=False))
    page.send_page()
