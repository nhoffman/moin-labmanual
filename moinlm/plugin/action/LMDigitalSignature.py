# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - Review Page Action

    This action sends a form prompting the user to review a page with
    provided comment.

    @copyright: 2008 Noah Hoffman <ngh2@uw.edu>
    @license: UW Free Fork
"""

import os
import re
import time
import sys
from MoinMoin import config, wikiutil
from MoinMoin.Page import Page

def execute(pagename, request):
    _ = request.getText

    if not request.user.may.write(pagename):
        request.theme.add_msg(_('You are not allowed to edit this page.'), "error")
        Page(request, pagename).send_page()
        return
    
    comment = request.form.get('statement', [''])[0] + ' ' + wikiutil.clean_input(request.form.get('comment', [''])[0])
    comment = comment.strip()
    
    if comment:
        from MoinMoin.PageEditor import PageEditor
        page = Page(request, pagename)
        pg = PageEditor(request, pagename)

        user = request.user.name

        msg = """<pre>
user: %(user)s

</pre>""" % locals()

        # save original page content with a comment
        savetext =  ('## reviewed/signed by %s %s \n' % (user, time.asctime())) + \
            page.get_raw_body().rstrip()
        rev = request.rev or 0
        try:
            pg.saveText(savetext, rev, trivial=False, comment=comment)
            msg = 'The page has been saved with the comment "%(comment)s".' % \
                locals()
        except Exception, msg:
            pass
    else:
        msg = """
    <form method="post" action="">
    <input type="hidden" name="action" value="LMDigitalSignature">
    <select name="statement">
      <option value="[REVIEWED]">[REVIEWED]</option>
      <option value="[REVIEWED+REVISED]">[REVIEWED+REVISED]</option>
      <option value="[REVIEWED+AUTHORIZED]">[REVIEWED+AUTHORIZED]</option>
      <option value="">(optional comment only)</option>
    </select>
    Optional comment:
    <input type="text" name="comment" value="" size="80" maxlength="80">
    <br/>

    <input type="submit" name="button" value="Submit">

    <ul>

    <li>This action is intended for content owners and represents a
    "digital signature" documenting that the content of the document
    has been reviewed and its contents approved.</li>

    <li>Please press the above button to document that you have
    reviewed this page or click "Clear message" below to cancel.</li>

    <li>A version of this page will be saved with the provided comment
    recorded in the revision history (view comments in the revision
    history using the "info" link below).</li>

    <li>Your name and the date/time will be recorded automatically - you do not need to enter them here.</li>

    </ul>
    </form>
    """ % locals()

    request.theme.add_msg(msg)
    Page(request, pagename).send_page()

