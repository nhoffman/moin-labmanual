# -*- coding: iso-8859-1 -*-

"""
   A macro for testing purposes

   $Rev: 3285 $
"""

import sys, os, re, time, datetime, pprint

from MoinMoin import search, wikiutil
from MoinMoin.logfile import editlog
from MoinMoin.Page import Page
from MoinMoin.util.dataset import TupleDataset, Column
from MoinMoin.widget.browser import DataBrowserWidget

from MoinMoin.user import User

Dependencies = ["time"]

def get_args(arguments, defaults, argstr):
    """
    @param arguments: list of argument names
    @param defaults: list of default values for argument keys
    @param argstr: string from the wiki markup <<NewPage(string)>>
    @rtype: dict
    @return: dictionary with macro options
    """

    argdict = dict(zip(arguments, defaults))

    if not argstr:
        return argdict

    args = [s.strip() for s in argstr.split(',')]
    argdict.update(dict(zip(arguments, args)))
    return argdict

def execute(self, argstr=''):

    request = self.request

    try:
        args, kwargs, trailing = wikiutil.parse_quoted_separated(argstr or u'')

        output = """
    <pre>
    argstr:   %(argstr)s
    args:     %(args)s
    kwargs:   %(kwargs)s
    trailing: %(trailing)s
    </pre>
    """ % locals()


        user = User(request,id='1217601938.86.28338').name

        return output

    except:
        return '<pre>%s</pre>' % pprint.pformat(sys.exc_info())

