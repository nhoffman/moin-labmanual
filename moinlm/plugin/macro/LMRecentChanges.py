# -*- coding: iso-8859-1 -*-

"""
    Macro that highlights enclosed text. Commas, semicolons, and other
    special characters are ok; wiki markup and html are not formatted.

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

def main(macro, args):

    request = macro.request
    _ = request.getText    
    
    try:
        if not args:
            raise ValueError('no value provided')

        #msg = _(args)
        msg = args
        
        output = request.formatter.text(args, style="color:red; font-weight: bold; font-style: italic;")

        return output
        
    except Exception, err:
        return macro.request.formatter.text(
            "<<LMRecentChanges: Error - %s>>" % err.args[0], style="color:red")
    

def execute(macro, args):
    try:
        return main(macro, args)
    except Exception, err:
        return macro.request.formatter.text(
            "<<LMRecentChanges: Error - %s>>" % err.args[0], style="color:red")


