# -*- coding: iso-8859-1 -*-

"""
    LM custom macro to list pages matching a pattern and identify
    modification times corresponding to matching log comments.

    derived from:
    MoinMoin/macro/__init__.py: _macro_PageList

    see also:
    MoinMoin/search/builtin.py
    MoinMoin/search/results.py
    MoinMoin/action/info.py

    $Rev: 3285 $
"""

import re
import time
import datetime

from MoinMoin import search, wikiutil
from MoinMoin.logfile import editlog
from MoinMoin.Page import Page
from MoinMoin.util.dataset import TupleDataset, Column
from MoinMoin.widget.browser import DataBrowserWidget

Dependencies = ["time"]

def main(macro, arg):

    request = macro.request
    _ = request.getText
    pagename = macro.formatter.page.page_name
    page = Page(request, pagename)

    msg = arg

#     <div style="border:red; border-style:dotted; padding:0.5em; background-color:#FFCCCC;">
#
# <u>Please note:</u>
# This wiki is <strong>read-only</strong> because it has been converted to a new MoinMoin wiki software version and also
# moved to a new URL. The new URL of the page requested by you is <b><a href="http://moinmo.in/HelpOnEditLocks">http://moinmo.in/HelpOnEditLocks</a></b>, please update your bookmarks.
#
# </div>

    output = request.formatter.text(msg, style="color:red; border-style:dotted; padding:0.5em; background-color:#FFCCCC; width:75%; display:block")
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


