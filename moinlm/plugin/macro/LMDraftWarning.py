# -*- coding: iso-8859-1 -*-

"""
    LMDraftWarning Macro

    Indicates that a page is in draft status.

    @copyright: 2010 Noah Hoffman <ngh2@uw.edu>
    @license: UW Free Fork
"""

from MoinMoin.logfile import editlog
from MoinMoin.Page import Page

from moinlm.utils import parse_args

Dependencies = ["time"]


def search_by_revision(request, pagename, rev):

    log = editlog.EditLog(request, rootpagename=pagename)
    rev = int(rev)

    matches = [line for line in log if rev == int(line.rev)]

    if matches:
        return matches[0].comment
    else:
        raise ValueError('This document has no revision number %s' % rev)


def execute(macro, argstr):

    request = macro.request
    _ = request.getText
    pagename = macro.formatter.page.page_name
    page = Page(request, pagename)

    style = ('color:red; border-style:dotted; '
             'padding:0.5em; background-color:#FFCCCC; '
             'width:75%%; display:block')

    try:
        args = parse_args(argstr, posargs=['comment', 'rev'])

        comment = args['comment']
        rev = args['rev']

        msg = 'Warning: this version is a draft. '

        if comment:
            msg += comment + '.'

        if rev:
            rev_link = page.link_to(
                request,
                text=_('revision %s' % rev, formatted=False),
                querystr='action=recall&rev=%s' % rev,
                rel='nofollow'
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
        return macro.request.formatter.text(
            "<<LMDraftWarning Error: %s>>" % err.args[0], style=style)
