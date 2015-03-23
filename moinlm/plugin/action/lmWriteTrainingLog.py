# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - Training Documentation Action

    This action adds a line to a log file indicating that the curent user
    has read the current page.

    @copyright: 2008 Noah Hoffman <ngh2@u.washington.edu>
    @license: UW Free Fork
"""

from MoinMoin.Page import Page
from MoinMoin.PageEditor import PageEditor
from MoinMoin.util import timefuncs

traininglog_fields = 'pagename rev user timestamp'.split()
traininglog_delim = ';'
traininglog_name = u"TrainingLog"


def read_training_log(request, pagename=None):
    logpage = Page(request, traininglog_name)
    lines = logpage.getlines()

    for line in lines:
        if not line.strip() or line.startswith('#'):
            continue

        d = dict(zip(traininglog_fields, line.split(traininglog_delim)))
        if not pagename:
            yield d
        elif d.get('pagename') == pagename:
            yield d


def record_training(request, page_info):
    editor = PageEditor(request, traininglog_name, do_revision_backup=0)
    raw_body = editor.get_raw_body_str()
    new_line = traininglog_delim.join(page_info[f] for f in traininglog_fields)
    editor.saveText(newtext=raw_body.strip() + '\n' + new_line, rev=0)


def execute(pagename, request):

    _ = request.getText
    page = Page(request, pagename)
    user = request.user

    page_info = page.lastEditInfo()
    page_info['rev'] = repr(page.get_real_rev())
    page_info['user'] = user.name
    page_info['pagename'] = pagename
    page_info['timestamp'] = timefuncs.W3CDate()

    record_training(request, page_info)

    msg_text = """Thank you! You have documented that you have read
    revision %(rev)s of "%(pagename)s"
    """ % page_info

    msg = _(msg_text, formatted=False)

    request.theme.add_msg(msg)
    page.send_page()
