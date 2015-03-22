# -*- coding: iso-8859-1 -*-

"""
    Macro LMPageList

    LM custom macro to list pages matching a pattern and identify
    modification times corresponding to matching log comments. This
    macro is useful when the wiki is used as a CMS, and it is
    necessary to periodically review pages.

    @param macro: current macro instance

    LMPageList may be passed the following arguments (positionally or
    using keywords)

    * page - (default "regex:.+") a pattern for matching page
      names. "-domain:system" is appended to exclude system pages.
    * comment - (default None) a pattern used to match comments in the revision
      history of each page.
    * interval - (default 365) Number of days after most revent
      revision or revision matching
      comment parameter that a page is considered "expired."
    * show - (default "all") Values of "expired" or "uptodate" show on the the
      corresponding pages.
    * editors - name of a group page containing a list of users

    derived from:
    MoinMoin/macro/PageList.py
"""

import sys
import re
import datetime
import pprint

from MoinMoin import search, wikiutil
from MoinMoin.logfile import editlog
from MoinMoin.user import User
from MoinMoin.util.dataset import TupleDataset, Column
from MoinMoin.widget.browser import DataBrowserWidget

Dependencies = ["time"]

grey = '<span style="color: grey">%s</span>'
yellow_bg = '<span style="background: yellow">%s</span>'
red_bg = '<span style="background: red">%s</span>'
green_bg = '<span style="background: green">%s</span>'

ok = '<span style="background: #33FF00">%s</span>'
flagged = '<span style="background: red; color: white">%s</span>'
highlight = '<span style="font-weight:bold; text-decoration:underline">%s</span>'


class Row(object):

    def __init__(self, request, log, log_rexp, interval, editors=None):
        """
        * request - Macro.request instance
        * log - an EditLog instance
        * log_rexp - used for matching comment lines
        * interval - acceptable interval for document review in days;
          to suppress highlighting, use value of 0
        * editors - set of user names; if provided, matching revisions
          must have been performed by a user in this set
        """

        # TODO: search against uiser ids instead of user names!

        self.rev = ''
        self.mdate = ''
        self.elapsed = ''
        self.editor = ''
        self.comment = grey % '(no matching revisions)'
        self.expired = False

        # restrict to a subset of revision actions
        ok_actions = set(['SAVE', 'SAVENEW', 'SAVE/REVERT', 'SAVE/RENAME'])
        lines = [line for line in log.reverse() if line.action in ok_actions]

        username = lambda x: User(request, id=x.userid).name

        if not lines:
            # self.comment = [username(line) for line in lines]
            return None

        most_recent_rev = int(lines[0].rev)

        if log_rexp:
            # perform search for matching comments
            log_re = re.compile(r'' + log_rexp, re.IGNORECASE)
            matches = [line for line in lines if log_re.search(line.comment)]

            if editors:
                matches = [line for line in matches if username(line) in editors]

            has_match = bool(matches)

            if has_match:
                line = matches[0]
            else:
                line = lines[0]

            self.rev = int(line.rev)
            if self.rev != most_recent_rev:
                self.rev = yellow_bg % ('%s (%s)' % (self.rev, most_recent_rev))
        else:
            # don't search rev history
            line = lines[0]
            self.rev = int(line.rev)

        self.line = line
        self.editor = line.getEditor(request)

        # elapsed time
        mtime = wikiutil.version2timestamp(line.ed_time_usecs)
        self.mdate = request.user.getFormattedDate(mtime)
        today = datetime.datetime.today()
        mDateTime = datetime.datetime.fromtimestamp(mtime)

        delta = today - mDateTime
        elapsed = str(delta)
        if 'days' in elapsed:
            self.elapsed = elapsed.split()[0]
        elif 'day' in elapsed:
            self.elapsed = '~ 1'
        else:
            self.elapsed = '< 1'

        if interval > 0 and delta > datetime.timedelta(days=interval):
            self.elapsed = yellow_bg % self.elapsed
            self.expired = True

        # comment field
        comment = line.comment
        if log_rexp:
            if has_match:
                # highlight matching substring
                comment = log_re.subn(lambda mo: highlight % mo.group(0), comment)[0]

                if self.expired:
                    self.comment = flagged % comment
                else:
                    self.comment = ok % comment
            else:
                self.comment = grey % line.comment
        else:
            self.comment = line.comment


def do_search(macro, page_rexp, log_rexp, interval, show, groupPage=None):

    request = macro.request
    _ = macro._
    case = 0

    # results contains output of the Search.run() method
    # (an instance of the SearchResults class)
    results = search.searchPages(macro.request, page_rexp,
                                 titlesearch=1, case=case, sort='page_name')
    hits = list(results.hits)

    if groupPage:
        editors = groupMembers(groupPage)
    else:
        editors = None

    if hits:
        history = TupleDataset()
        history.columns = [
            Column('page', label='page', align='left'),
            Column('rev', label='rev', align='right'),
            Column('mdate', label=_('Date', formatted=False), align='right'),
            Column('elapsed', label=_('Elapsed', formatted=False), align='right'),
            Column('editor', label=_('Editor', formatted=False),
                   hidden=not request.cfg.show_names),
            Column('comment', label=_('Comment', formatted=False)),
            Column('action', label=_('Action', formatted=False)),
            ]

        for hit in hits:
            page = hit.page
            pagename = hit.page_name

            # exclude deprecated pages
            if 'deprecated' in [e[0] for e in page.meta]:
                continue

            row = Row(request, editlog.EditLog(request, rootpagename=pagename),
                      log_rexp, interval, editors)

            # exclude pages according to show parameter
            if (show == 'expired' and not row.expired) or \
               (show == 'uptodate' and row.expired):
                continue

            history.addRow((
                page.link_to(request),  # pagename
                row.rev,  # rev
                row.mdate,  # mdate
                row.elapsed,
                row.editor,  # editor
                row.comment,  # comment
                page.link_to(request, querystr='action=info', text='info')  # action
                ))

        history_table = DataBrowserWidget(request)
        history_table.setData(history)
        return history_table.render()
    else:
        return ''


def execute(self, argstr=''):

    # If called with empty or no argument, default to regex search
    # for .+, the full page list.

    request = self.request
    _ = self._

    def format_err(msg):
        style = """color:red; border-style:dotted; padding:0.5em;
            background-color:#FFCCCC; width:75%; display:block"""

        return request.formatter.text(
            ('Error in <<LMPageList(%s)>> ' % argstr) + msg,
            style=style)

    try:
        defaults = (
            ('page', 'regex:.+'),
            ('comment', None),
            ('interval', 365),
            ('show', 'all'),
            ('editors', None))
        keys = [x[0] for x in defaults]

        args = dict(defaults)
        positional, kwargs, trailing = wikiutil.parse_quoted_separated(argstr or u'')

        args.update(dict((k, v) for k, v in zip(keys, positional) if v))
        args.update(kwargs)

        page_rexp = args['page'] + ' -domain:system'
        log_rexp = args['comment'] or None

        # With whitespace argument, return same error message as FullSearch
        if page_rexp.isspace():
            return format_err(
                'Please use a more selective search term instead of {{{"%s"}}}',
                page_rexp)

        show = args['show']
        showvals = ['all', 'expired', 'uptodate']
        if show not in showvals:
            return format_err(
                'The argument "show" must have one of the following values: %s' %
                ', '.join(showvals))

        groupPageName = args['editors']
        if groupPageName:
            # search for this page, error if not found
            results = search.searchPages(request, groupPageName,
                                         titlesearch=1, case=1, sort='page_name')
            hits = list(results.hits)
            if not hits:
                return format_err(
                    '"editors" must be provided the name of an existing group page')
            groupPage = hits[0].page
        else:
            groupPage = None

        try:
            interval = float(args['interval'])
        except ValueError:
            return format_err('Interval must be a number of days')

        html = ' '
        # html += """\
        #       <pre>
        #        argstr:         %(argstr)s
        #        positional:     %(positional)s
        #        kwargs:         %(kwargs)s
        #        args:           %(args)s

        #        page_rexp:      %(page_rexp)s
        #        log_rexp:       %(log_rexp)s
        #        interval:       %(interval)s
        #        show:           %(show)s
        #        groupPageName:  %(groupPageName)s
        #        </pre>""" % locals()

        html += do_search(self, page_rexp, log_rexp, interval,
                          show=show, groupPage=groupPage)

        output = ['The table below can be described as follows:']
        output += ['<ol>']
        if html:
            if page_rexp.startswith('regex:.+ '):
                output.append(
                    """<li>Pages are shown without restriction on page name.</li>""")
            else:
                output.append("""<li>Pages below match the search term
                "<b>%(page)s</b>"</li>""" % args)

            if show == 'expired':
                output.append('<li>Only pages in need of revision are shown.</li>')
            elif show == 'uptodate':
                output.append('<li>Only up to date pages are shown.</li>')

            if log_rexp:
                output.append("""
            <li>The most recent log entry matching
            the search term "<b>%(log_rexp)s</b>" is shown (or the
            most recent entry if no match).</li>""" % locals())
                output.append("""<li>Revision numbers are highlighted
            if there were changes since the matching revision (most
            recent revision in parentheses).</li>
            """)
            else:
                output.append(
                    '<li>The most recent log entry for each page is shown.</li>')

            output.append(
                '<li>Elapsed time since the displayed revision is shown in days.</li>')

            if interval > 0:
                output.append(
                    '<li>Intervals > <b>%(interval)i</b> days are highlighted</li>' % locals())

            if groupPage:
                output.append("""<li>Only revisions performed by users
             listed in the page %s are shown</li>""" % groupPage.link_to(request))

            output.append('</ol>')

            output.append(html)
        else:
            output.append('LMPageList: No pages match the search term provided.</p>')

        return '\n'.join(output)

    except:
        return '<pre>%s</pre>' % pprint.pformat(sys.exc_info())


def groupMembers(groupPage):
    """
    Return set of member names (strings) in Page object groupPage
    """

    pageStr = groupPage.get_body()
    members = set(x.split()[-1] for x in pageStr.splitlines() if x.startswith(' * '))

    return members
