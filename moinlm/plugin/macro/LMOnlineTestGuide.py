# -*- coding: iso-8859-1 -*-

"""
    LMOnlineTestGuide Macro

    Generates a link to the Lab Medicine Online Test Guide

    @copyright: 2010 Noah Hoffman <ngh2@uw.edu>
    @license: UW Free Fork    
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

def execute(macro, args):

    request = macro.request
    _ = request.getText
    pagename = macro.formatter.page.page_name
    page = Page(request, pagename)
        
    try:
        defaults = (
            ('mnemonic',''),
            )
        keys = [x[0] for x in defaults]        
        argv = dict(defaults)

        positional, kwargs, trailing = wikiutil.parse_quoted_separated(args or u'')
        
        argv.update(dict((k,v) for k,v in zip(keys,positional) if v))
        argv.update(kwargs)
        
        mnemonic = argv['mnemonic']

        if not mnemonic:
            raise Exception('no mnemonic provided')
        
        #url = 'http://byblos.labmed.washington.edu/bcard/Form.asp?DataAction=ResetRC&Search=Mnemonic&Query='
        url = 'http://menu.labmed.washington.edu/'
        link = '<a href="%(url)s%(mnemonic)s" target=_blank>%(mnemonic)s</a>' % locals()
        
        return link
        
    except Exception, err:
        style = """color:red; border-style:dotted;
                padding:0.5em; background-color:#FFCCCC;
                width:75%%; display:block"""

        return macro.request.formatter.text(
            "<<LMOnlineTestGuide Error: %s>>" % err.args[0], style=style)
        
