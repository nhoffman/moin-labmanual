# -*- coding: iso-8859-1 -*-

"""
    Macro LMTrackerLink

    Return html-formatted link to an issue in a tracker.
"""

import sys
import re
import time
import datetime
import pprint

from MoinMoin import search, wikiutil
from MoinMoin.logfile import editlog
from MoinMoin.Page import Page
from MoinMoin.user import User
from MoinMoin.util.dataset import TupleDataset, Column
from MoinMoin.widget.browser import DataBrowserWidget

__version__ = "$Rev: 3322 $"

Dependencies = ["time"]


def execute(self, argstr=None):

    argstr = argstr or ''

    request = self.request
    _ = self._

    def format_err(msg):
        style = """color:red; border-style:dotted; padding:0.5em;
            background-color:#FFCCCC; width:75%; display:block"""

        return request.formatter.text(
            ('Error in <<LMTrackerLink(%s)>> '%argstr) + msg,
            style=style)

    try:
        defaults = (
            ('issue',None),
            ('tracker','it'),
        )
        keys = [x[0] for x in defaults]

        args = dict(defaults)
        positional, kwargs, trailing = wikiutil.parse_quoted_separated(argstr or u'')

        args.update(dict((k,v) for k,v in zip(keys,positional) if v))
        args.update(kwargs)

        if not args['issue']:
            return format_err('Please provide a tracker issue number')

        url = """
        <a href="https://web.labmed.washington.edu/tracker/%(tracker)s/roundup.cgi/%(tracker)s/issue%(issue)s"
        target="_blank">
        %(tracker)s:Issue%(issue)s
        </a>
        """ % args

        return url

    except:
        return '<pre>%s</pre>' % pprint.pformat(sys.exc_info())





