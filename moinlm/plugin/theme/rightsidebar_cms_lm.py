# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - modernized_cms theme

    @copyright: 2009 MoinMoin:ThomasWaldmann
    @license: GNU GPL, see COPYING for details.
"""

# from MoinMoin.theme.modernized import Theme as ThemeBase
from MoinMoin.theme.rightsidebar import Theme as ThemeBase

class Theme(ThemeBase):

    name = "rightsidebar_lm" # we tell that we are 'modernized', so we use its static data

    def wikipanel(self, d):
        """ Create wiki panel """
        _ = self.request.getText
        html = [
            u'<div class="sidepanel">',
            u'<h1>%s</h1>' % _("Pages"),
            self.navibar(d),
            u'</div>',
            ]
        return u'\n'.join(html)    


    def header(self, d):
        """
        Assemble page header

        @param d: parameter dictionary
        @rtype: string
        @return: page header html
        """
        _ = self.request.getText

        html = [
            # Custom html above header
            self.emit_custom_html(self.cfg.page_header1),

            # Header
            u'<div id="header">',
            # self.searchform(d),
            # self.logo(),
            # self.emit_custom_html(self.cfg.logo_string),
            u'<div id="locationline">',
            self.emit_custom_html(u'''<span class="logostr">&nbsp;%s</span>''' % self.cfg.logo_string),
            # self.emit_custom_html(self.cfg.logo_string),
            # self.interwiki(d),
            # self.title(d),
            u'</div>',
            # self.trail(d),
            u'</div>',

            # Custom html below header (not recomended!)
            self.emit_custom_html(self.cfg.page_header2),

            # Sidebar
            u'<div id="sidebar">',
            self.wikipanel(d),
            self.pagepanel(d),
            self.userpanel(d),
            u'</div>',

            self.msg(d),

            # Page
            self.startPage(),
            ]
        return u'\n'.join(html)

    
    def onlyloggedin(method):
        """ decorator that returns empty string for not logged-in users,
            otherwise it calls the decorated method
        """
        return lambda self, *args, **kwargs: ''

    # suppress other sidebar elements
    pagepanel = onlyloggedin(ThemeBase.pagepanel)
    userpanel = onlyloggedin(ThemeBase.userpanel)
    
    interwiki = onlyloggedin(ThemeBase.interwiki)
    # title = onlyloggedin(ThemeBase.title)
    username = onlyloggedin(ThemeBase.username)
    pageinfo = onlyloggedin(ThemeBase.pageinfo)
    editbar = onlyloggedin(ThemeBase.editbar)
    searchform = onlyloggedin(ThemeBase.searchform)

def execute(request):
    return Theme(request)

