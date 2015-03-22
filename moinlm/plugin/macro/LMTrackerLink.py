# -*- coding: iso-8859-1 -*-

"""
    Macro LMTrackerLink

    Return html-formatted link to an issue in a tracker.
"""

import sys
import pprint

from MoinMoin import wikiutil

Dependencies = ["time"]


def execute(self, argstr=None):

    argstr = argstr or ''

    request = self.request

    def format_err(msg):
        style = """color:red; border-style:dotted; padding:0.5em;
            background-color:#FFCCCC; width:75%; display:block"""

        return request.formatter.text(
            ('Error in <<LMTrackerLink(%s)>> ' % argstr) + msg, style=style)

    try:
        defaults = (
            ('issue', None),
            ('tracker', 'it'),
        )
        keys = [x[0] for x in defaults]

        args = dict(defaults)
        positional, kwargs, trailing = wikiutil.parse_quoted_separated(argstr or u'')

        args.update(dict((k, v) for k, v in zip(keys, positional) if v))
        args.update(kwargs)

        if not args['issue']:
            return format_err('Please provide a tracker issue number')

        url = """
        <a href="https://tracker.labmed.uw.edu/%(tracker)s/issue%(issue)s"
        target="_blank">
        %(tracker)s:Issue%(issue)s
        </a>
        """ % args

        return url

    except:
        return '<pre>%s</pre>' % pprint.pformat(sys.exc_info())
