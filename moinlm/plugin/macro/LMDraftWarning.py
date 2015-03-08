# -*- coding: iso-8859-1 -*-

"""
    LMDraftWarning Macro

    Indicates that a page is in draft status.

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

def search_by_revision(request, pagename, rev):

    log = editlog.EditLog(request, rootpagename=pagename)
    rev = int(rev)
    
    matches = [line for line in log \
                    if rev==int(line.rev)]

    if matches:
        return matches[0].comment
    else:
        raise ValueError('This document has no revision number %s' % rev)

def execute(macro, args):

    request = macro.request
    _ = request.getText
    pagename = macro.formatter.page.page_name
    page = Page(request, pagename)
    
    def render_action(text, query, **kw):
        kw.update(dict(rel='nofollow'))
        return page.link_to(request, text, querystr=query, **kw)
    
    def format_err(msg):
        style = """color:red; border-style:dotted; padding:0.5em;
            background-color:#FFCCCC; width:75%; display:block"""

        return request.formatter.text(
            ('Error in <<LMPageList(%s)>> '%argstr) + msg,
            style=style)
    
    try:
        defaults = (
            ('comment',''),
            ('rev',None)
            )
        keys = [x[0] for x in defaults]        
        argv = dict(defaults)

        positional, kwargs, trailing = wikiutil.parse_quoted_separated(args or u'')
        
        argv.update(dict((k,v) for k,v in zip(keys,positional) if v))
        argv.update(kwargs)

        msg = 'Warning: this version is a draft. '
        
        comment = argv['comment']
        rev = argv['rev']
        
        if comment:
            msg += comment + '.'

        style = """color:red; border-style:dotted;
                padding:0.5em; background-color:#FFCCCC;
                width:75%%; display:block"""
            
        if rev:
            rev_link = page.link_to(
                request,
                text=_('revision %s' % rev, formatted=False),
                querystr = 'action=recall&rev=%s' % rev,
                rel= 'nofollow'
                )
            rev_comment = search_by_revision(request, pagename, rev)
            
            msg += """ Please refer to %%s of this
            document, which was saved with the comment "%s"
        """ % rev_comment

            output = request.formatter.text(msg, style=style) % rev_link            
        else:
            output = request.formatter.text(msg, style=style)
        
        return output + '<br/>'
        
    except Exception, err:
        style = """color:red; border-style:dotted;
                padding:0.5em; background-color:#FFCCCC;
                width:75%%; display:block"""

        return macro.request.formatter.text(
            "<<LMDraftWarning Error: %s>>" % err.args[0], style=style)
        
