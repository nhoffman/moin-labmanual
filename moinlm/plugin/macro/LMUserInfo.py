# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - SystemInfo Macro

    This macro shows some info about your wiki, wiki software and your system.

    @copyright: 2006 MoinMoin:ThomasWaldmann,
                2007 MoinMoin:ReimarBauer
    @license: GNU GPL, see COPYING for details.

    $Rev: 3285 $
    """

Dependencies = ['pages']

import sys, os
from StringIO import StringIO

from MoinMoin import wikiutil, version
from MoinMoin import action, macro, parser
from MoinMoin.logfile import editlog, eventlog
from MoinMoin.Page import Page

class UserInfo:
    def __init__(self, macro, args):
        self.macro = macro
        self.request = macro.request
        self.formatter = macro.formatter
        self.args = args

    def render(self):
        _ = self.request.getText
        return self.formatter.rawHTML(self.getInfo())

    def getInfo(self):
        _ = self.request.getText
        request = self.request

        buf = StringIO()

        row = lambda label, value, buf=buf: buf.write(u'<dt>%s</dt><dd>%s</dd>' % (label, value))

        buf.write(u'<dl>')

        for attr in 'name valid isSuperUser auth_method auth_username auth_attribs'.split():
        ## for attr in dir(request.user):
            if attr.startswith('_'):
                continue

            try:
                val = getattr(request.user,attr)()
            except:
                val = getattr(request.user,attr) or `getattr(request.user,attr)`
            row('request.user.%s'%attr,_(val, formatted=False))

        # row('dir(request.user)',_(`dir(request.user)`, formatted=False))

        return buf.getvalue()

def execute(macro, args):
    if macro.request.isSpiderAgent: # reduce bot cpu usage
        return ''
    return UserInfo(macro, args).render()



