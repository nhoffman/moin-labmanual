"""LMPageList

Macro for displaying approval status for a list of pages.

Options:


"""

from itertools import ifilter, chain
from operator import attrgetter
from collections import namedtuple
import re
from datetime import datetime
from functools import partial

from jinja2 import Template
from MoinMoin import search, wikiutil
from MoinMoin.Page import Page
from MoinMoin.user import User
from MoinMoin.logfile import editlog

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


def get_last_approved(request, log, log_re=None, approvers=None):
    """
    * request - Macro.request instance
    * log - an EditLog instance
    * log_re - compiled regular expression used for matching comment lines
    * approvers - set of user names; if provided, matching revisions
      must have been performed by a user in this set
    """

    # restrict to a subset of revision actions
    ok_actions = {'SAVE', 'SAVENEW', 'SAVE/REVERT', 'SAVE/RENAME'}
    lines = (line for line in log.reverse() if line.action in ok_actions)

    # perform search for matching comments
    if log_re:
        lines = (line for line in lines if log_re.search(line.comment))

    if approvers:
        lines = (line for line in lines if get_editor(request, line) in approvers)

    try:
        firstmatch = next(lines)
    except StopIteration:
        firstmatch = None

    return firstmatch


def get_elapsed_since_edit(line):
    """Return an instance of datetime.timedelta indicating time elapsed
    given an instance of MoinMoin.logfile.editlog.EditLogLine

    """

    today = datetime.today()
    mtime = wikiutil.version2timestamp(line.ed_time_usecs)
    mdate_time = datetime.fromtimestamp(mtime)
    delta = today - mdate_time
    return delta


def get_modification_date(line):
    mtime = wikiutil.version2timestamp(line.ed_time_usecs)
    return datetime.fromtimestamp(mtime)


PageStatus = namedtuple('PageStatus', [
    'page',
    'rev',
    'rev_class',
    'author',
    'date',
    'elapsed',
    'is_approved',
    'comment',
    'comment_class',
])


def get_page_status(page, request, log_rexp=None, approvers=None, interval=None):

    log = editlog.EditLog(request, rootpagename=page.page_name)
    current = next(log.reverse())
    current_rev = int(current.rev)
    log_re = re.compile(r'' + log_rexp, re.IGNORECASE) if log_rexp else None

    last_approved = get_last_approved(
        request, log=log, log_re=log_re, approvers=approvers)

    if last_approved:
        last_approved_rev = int(last_approved.rev)

        if current_rev == last_approved_rev:
            rev = '{}'.format(current_rev)
            rev_class = ''
        else:
            rev = '{} ({})'.format(last_approved_rev, current_rev)
            rev_class = 'modified'

        author = get_editor(request, last_approved)
        elapsed = get_elapsed_since_edit(last_approved)
        is_approved = elapsed.days <= interval if interval else True
        comment_class = 'approved' if is_approved else 'expired'
        date = get_modification_date(last_approved)
        if log_rexp:
            comment = log_re.sub(
                lambda mobj: '<span class="matched">{}</span>'.format(mobj.group(0)),
                last_approved.comment)
        else:
            comment = last_approved.comment
    else:
        rev = current_rev
        rev_class = ''
        author = get_editor(request, current)
        elapsed = get_elapsed_since_edit(current)
        is_approved = False
        comment_class = 'unapproved'
        date = get_modification_date(current)
        comment = current.comment

    return PageStatus(
        page=page,
        rev=rev,
        rev_class=rev_class,
        author=author,
        date=date,
        elapsed=elapsed.days if elapsed.days >= 1 else '< 1',
        is_approved=is_approved,
        comment=comment,
        comment_class=comment_class,
    )


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

    # define a callable that returns page status given params passed to main()
    get_status = partial(
        get_page_status, request=request,
        log_rexp=log_rexp, approvers=approvers, interval=interval)

    # Search for pages matching 'pattern'; result contains output of
    # the Search.run() method (an instance of the SearchResults class)
    result = search.searchPages(
        request,
        query=page_rexp,
        titlesearch=True,
        case=False,
        sort='page_name')

    pages = (hit.page for hit in result.hits)
    pagestatus = (get_status(page) for page in pages)

    template = Template("""
<style>
  tr.unapproved { color: grey; }
  td.approved { background: #33FF00; }
  td.expired { background: red; color: white; }
  td.unapproved { color: grey; }
  td.modified { background: yellow; }
  span.matched { font-weight: bold; text-decoration: underline; }
</style>
<table>
  <tr>
    <th>Page</th>
    <th>Rev</th>
    <th>Date</th>
    <th>Elapsed</th>
    <th>Editor</th>
    <th>Comment</th>
    <th>Action</th>
  </tr>
  {% for page in pagestatus %}
    <tr{% if not page.is_approved %} class="unapproved"{% endif %}>
      <td>{{ page.page.link_to(request) }}</td>
      <td class="{{ page.rev_class }}">{{ page.rev }}</td>
      <td>{{ page.date.strftime('%Y-%m-%d') }}</td>
      <td>{{ page.elapsed }}</td>
      <td>{{ page.author or '' }}</td>
      <td class="{{ page.comment_class }}">{{ page.comment }}</td>
      <td>
    {{ page.page.link_to(request, querystr='action=info', text='info') }}
    {{ page.page.link_to(request,
       querystr='action=LMDigitalSignature', text='sign') }}
      </td>
    </tr>
{% endfor %}
</table>

    """)

    return template.render(
        pagestatus=pagestatus,
        request=request,
    )


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
