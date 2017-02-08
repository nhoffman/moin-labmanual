"""LMPageList

Macro for displaying approval status for a list of pages.

Options:


"""

from itertools import ifilter, chain
from operator import attrgetter
import re

from jinja2 import Template
from MoinMoin import wikiutil
from MoinMoin.Page import Page
from MoinMoin.user import User

Dependencies = ["time"]


def group_from_page(request, pagename):
    page = Page(request, pagename)
    if not page.exists():
        raise ValueError('The page "{}" does not exist'.format(pagename))
    return {line.split()[-1]
            for line in page.get_body().splitlines()
            if line.strip().startswith('*')}


def get_editor(request, logline):
    return User(request, id=logline.userid).name


def filter_log(request, log, log_rexp=None, approvers=None):
    """
    * request - Macro.request instance
    * log - an EditLog instance
    * log_rexp - used for matching comment lines
    * approvers - set of user names; if provided, matching revisions
      must have been performed by a user in this set
    """

    # restrict to a subset of revision actions
    ok_actions = {'SAVE', 'SAVENEW', 'SAVE/REVERT', 'SAVE/RENAME'}
    lines = (line for line in log.reverse() if line.action in ok_actions)

    # perform search for matching comments
    if log_rexp:
        log_re = re.compile(r'' + log_rexp, re.IGNORECASE)
        lines = (line for line in lines if log_re.search(line.comment))

    if approvers:
        lines = (line for line in lines if get_editor(request, line) in approvers)

    try:
        firstmatch = next(lines)
    except StopIteration:
        firstmatch = None

    return firstmatch


def main(macro, pattern='regex:.+', comment=None, interval=365, show='all',
         editors=None, show_help=False):

    if show_help:
        return '<pre>{}</pre>'.format(__doc__)

    request = macro.request

    # With whitespace argument, return same error message as FullSearch
    if not pattern or pattern.isspace() or pattern in {'""', "''"}:
        raise ValueError('Please use a more selective search term for "pattern"')

    showvals = {'all', 'expired', 'uptodate'}
    if show not in showvals:
        raise ValueError(
            'The argument "show" must have one of the following values: ' +
            ', '.join(showvals))

    approvers = group_from_page(editors) if editors else None

    page_rexp = pattern + ' -domain:system'
    log_rexp = comment or None

    template = Template("""
    foo
    """)

    msg = template.render(
    )
    return msg


def execute(macro, argstr):
    try:
        if argstr:
            args, kwargs, trailing = wikiutil.parse_quoted_separated(argstr)
        else:
            args, kwargs, trailing = tuple(), {}, None
        if trailing:
            raise ValueError('trailing arguments are not allowed')
        return main(macro, *args, **kwargs)
    except Exception, err:
        msg = err.args[0] if err.args else 'Error'
        return macro.request.formatter.text(
            "<<LMPageList({})>>: {}".format(argstr, msg), style="color:red")
