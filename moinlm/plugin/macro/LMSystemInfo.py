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

class SystemInfo:
    def __init__(self, macro, args):
        self.macro = macro
        self.request = macro.request
        self.formatter = macro.formatter
        self.args = args

    def formatInReadableUnits(self, size):
        size = float(size)
        unit = u' Byte'
        if size > 9999:
            unit = u' KiB'
            size /= 1024
        if size > 9999:
            unit = u' MiB'
            size /= 1024
        if size > 9999:
            unit = u' GiB'
            size /= 1024
        return u"%.1f %s" % (size, unit)

    def getDirectorySize(self, path):
        try:
            dirsize = 0
            for root, dummy, files in os.walk(path):
                dirsize += sum([os.path.getsize(os.path.join(root, name)) for name in files])
        except EnvironmentError:
            dirsize = -1
        return dirsize

    def render(self):
        _ = self.request.getText
        return self.formatter.rawHTML(self.getInfo())

    def getInfo(self):
        _ = self.request.getText
        request = self.request

        buf = StringIO()

        row = lambda label, value, buf=buf: buf.write(u'<dt>%s</dt><dd>%s</dd>' % (label, value))

        buf.write(u'<dl>')
        row(_('Python Version', formatted=False), sys.version)
        row(_('MoinMoin Version', formatted=False), _('Release %s [Revision %s]', formatted=False) % (version.release, version.revision))

        if not request.user.valid:
            # for an anonymous user it ends here.
            buf.write(u'</dl>')
            return buf.getvalue()

        if request.user.isSuperUser():
            # superuser gets all page dependent stuff only
            try:
                import Ft
                ftversion = Ft.__version__
            except ImportError:
                ftversion = None
            except AttributeError:
                ftversion = 'N/A'

            if ftversion:
                row(_('4Suite Version', formatted=False), ftversion)

            # TODO add python-xml check and display it

            # Get the full pagelist of the wiki
            pagelist = request.rootpage.getPageList(user='')
            systemPages = []
            totalsize = 0
            for page in pagelist:
                if wikiutil.isSystemPage(request, page):
                    systemPages.append(page)
                totalsize += Page(request, page).size()

            row(_('Number of pages', formatted=False), str(len(pagelist)-len(systemPages)))
            row(_('Number of system pages', formatted=False), str(len(systemPages)))

            row(_('Accumulated page sizes', formatted=False), self.formatInReadableUnits(totalsize))
            data_dir = request.cfg.data_dir
            row(_('Disk usage of %(data_dir)s/pages/', formatted=False) % {'data_dir': data_dir},
                self.formatInReadableUnits(self.getDirectorySize(os.path.join(data_dir, 'pages'))))
            row(_('Disk usage of %(data_dir)s/', formatted=False) % {'data_dir': data_dir},
            self.formatInReadableUnits(self.getDirectorySize(data_dir)))

            edlog = editlog.EditLog(request)
            row(_('Entries in edit log', formatted=False), "%s (%s)" % (edlog.lines(), self.formatInReadableUnits(edlog.size())))

            # This puts a heavy load on the server when the log is large
            eventlogger = eventlog.EventLog(request)
            row('Event log', self.formatInReadableUnits(eventlogger.size()))

        nonestr = _("NONE", formatted=False)
        # a valid user gets info about all installed extensions
        row(_('Global extension macros', formatted=False), ', '.join(macro.modules) or nonestr)
        row(_('Local extension macros', formatted=False),
            ', '.join(wikiutil.wikiPlugins('macro', self.macro.cfg)) or nonestr)

        glob_actions = [x for x in action.modules
                        if not x in request.cfg.actions_excluded]
        row(_('Global extension actions', formatted=False), ', '.join(glob_actions) or nonestr)
        loc_actions = [x for x in wikiutil.wikiPlugins('action', self.macro.cfg)
                       if not x in request.cfg.actions_excluded]
        row(_('Local extension actions', formatted=False), ', '.join(loc_actions) or nonestr)

        row(_('Global parsers', formatted=False), ', '.join(parser.modules) or nonestr)
        row(_('Local extension parsers', formatted=False),
            ', '.join(wikiutil.wikiPlugins('parser', self.macro.cfg)) or nonestr)

        from MoinMoin.search.builtin import Search
        xapState = (_('Disabled', formatted=False), _('Enabled', formatted=False))
        idxState = (_('index available', formatted=False), _('index unavailable', formatted=False))
        xapRow = xapState[request.cfg.xapian_search]

        if request.cfg.xapian_search:
            idx = Search._xapianIndex(request)
            available = idx and idxState[0] or idxState[1]
            mtime = _('last modified: %s', formatted=False) % (idx and
                request.user.getFormattedDateTime(
                    wikiutil.version2timestamp(idx.mtime())) or
                    _('N/A', formatted=False))
            xapRow += ', %s, %s' % (available, mtime)

        try:
            import xapian
            try:
                xapVersion = xapian.version_string()
            except AttributeError:
                xapVersion = xapian.xapian_version_string() # deprecated since xapian 0.9.6, removal in 1.1.0
#         except ImportError:
#             xapVersion = _('Xapian and/or Python Xapian bindings not installed', formatted=False)
        except ImportError, msg:
            xapVersion = _('Xapian and/or Python Xapian bindings not installed: %s' % msg, formatted=False)

        row(_('Xapian search', formatted=False), xapRow)
        row(_('Xapian Version', formatted=False), xapVersion)

        stems = [nonestr]
        try:
            import Stemmer
            try:
                stems = Stemmer.algorithms()
                stemVersion = Stemmer.version()
            except:
                 stemVersion = _('PyStemmer not installed', formatted=False)
        except ImportError:
            stemVersion = _('PyStemmer not installed', formatted=False)

        row(_('Stemming for Xapian', formatted=False), xapState[request.cfg.xapian_stemming])
        row(_('PyStemmer Version', formatted=False), stemVersion)
        row(_('PyStemmer stems', formatted=False), ', '.join(stems) or nonestr)

        try:
            from threading import activeCount
            t_count = activeCount()
        except ImportError:
            t_count = None

        row(_('Active threads', formatted=False), t_count or _('N/A', formatted=False))

        ## NH added these
        for env_var in 'PWD LD_LIBRARY_PATH'.split():
        #for env_var in sorted(os.environ.keys()):
            row(_(env_var, formatted=False), os.environ.get(env_var,'not defined'))

        buf.write(u'</dl>')

        return buf.getvalue()

def execute(macro, args):
    if macro.request.isSpiderAgent: # reduce bot cpu usage
        return ''
    return SystemInfo(macro, args).render()

