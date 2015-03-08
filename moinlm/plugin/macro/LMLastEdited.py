# -*- coding: iso-8859-1 -*-

"""
Prints user and date associated with the last edit of the current page.
"""

import re
import time
import datetime

from MoinMoin import search, wikiutil
from MoinMoin.logfile import editlog
from MoinMoin.Page import Page

Dependencies = ["time"]

def main(macro):

    request = macro.request
    _ = request.getText
    pagename = macro.formatter.page.page_name
    page = Page(request, pagename)

    log = editlog.EditLog(request, rootpagename=pagename)
    last_edit = list(log)[-1]
    mtime = wikiutil.version2timestamp(last_edit.ed_time_usecs)
    mdate = request.user.getFormattedDate(mtime)

    msg = _('Page last modified %s' % mdate)

    output = request.formatter.text(msg, style="color:grey; float:right;")
    return output

def execute(macro, args):
    try:
        return wikiutil.invoke_extension_function(
                   macro.request, main,
                   args, [macro])
    except ValueError, err:
        return macro.request.formatter.text(
            "<<LMWarningBox: %s>>" % err.args[0], style="color:red")



#     import urllib
#     fstr = """
#     <pre>%s</pre>
#     """
#     features = [
#     time.asctime(),
#     dir(results),
#     results.estimated_hits
#     ]
#     return ''.join([fstr % f for f in features])


