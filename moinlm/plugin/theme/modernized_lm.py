# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - modern theme

    @copyright: 2003-2005 Nir Soffer, Thomas Waldmann
    @license: GNU GPL, see COPYING for details.
"""

from MoinMoin.theme import ThemeBase
from MoinMoin import wikiutil
from MoinMoin.Page import Page
from MoinMoin.action import get_available_actions


class Theme(ThemeBase):

    name = "modernized"

    _ = lambda x: x  # We don't have gettext at this moment, so we fake it
    icons = {
        # key         alt                        icon filename      w   h
        # FileAttach
        'attach': ("%(attach_count)s", "moin-attach.png", 16, 16),
        'info': ("[INFO]", "moin-info.png", 16, 16),
        'attachimg': (_("[ATTACH]"), "attach.png", 32, 32),
        # RecentChanges
        'rss': (_("[RSS]"), "moin-rss.png", 16, 16),
        'deleted': (_("[DELETED]"), "moin-deleted.png", 16, 16),
        'updated': (_("[UPDATED]"), "moin-updated.png", 16, 16),
        'renamed': (_("[RENAMED]"), "moin-renamed.png", 16, 16),
        'conflict': (_("[CONFLICT]"), "moin-conflict.png", 16, 16),
        'new': (_("[NEW]"), "moin-new.png", 16, 16),
        'diffrc': (_("[DIFF]"), "moin-diff.png", 16, 16),
        # General
        'bottom': (_("[BOTTOM]"), "moin-bottom.png", 16, 16),
        'top': (_("[TOP]"), "moin-top.png", 16, 16),
        'www': ("[WWW]", "moin-www.png", 16, 16),
        'mailto': ("[MAILTO]", "moin-email.png", 16, 16),
        'news': ("[NEWS]", "moin-news.png", 16, 16),
        'telnet': ("[TELNET]", "moin-telnet.png", 16, 16),
        'ftp': ("[FTP]", "moin-ftp.png", 16, 16),
        'file': ("[FILE]", "moin-ftp.png", 16, 16),
        # search forms
        'searchbutton': ("[?]", "moin-search.png", 16, 16),
        'interwiki': ("[%(wikitag)s]", "moin-inter.png", 16, 16),

        # smileys (this is CONTENT, but good looking smileys depend on looking
        # adapted to the theme background color and theme style in general)
        # vvv    ==      vvv  this must be the same for GUI editor converter
        'X-(': ("X-(", 'angry.png', 16, 16),
        ':D': (":D", 'biggrin.png', 16, 16),
        '<:(': ("<:(", 'frown.png', 16, 16),
        ':o': (":o", 'redface.png', 16, 16),
        ':(': (":(", 'sad.png', 16, 16),
        ':)': (":)", 'smile.png', 16, 16),
        'B)': ("B)", 'smile2.png', 16, 16),
        ':))': (":))", 'smile3.png', 16, 16),
        ';)': (";)", 'smile4.png', 16, 16),
        '/!\\': ("/!\\", 'alert.png', 16, 16),
        '<!>': ("<!>", 'attention.png', 16, 16),
        '(!)': ("(!)", 'idea.png', 16, 16),
        ':-?': (":-?", 'tongue.png', 16, 16),
        ':\\': (":\\", 'ohwell.png', 16, 16),
        '>:>': (">:>", 'devil.png', 16, 16),
        '|)': ("|)", 'tired.png', 16, 16),
        ':-(': (":-(", 'sad.png', 16, 16),
        ':-)': (":-)", 'smile.png', 16, 16),
        'B-)': ("B-)", 'smile2.png', 16, 16),
        ':-))': (":-))", 'smile3.png', 16, 16),
        ';-)': (";-)", 'smile4.png', 16, 16),
        '|-)': ("|-)", 'tired.png', 16, 16),
        '(./)': ("(./)", 'checkmark.png', 16, 16),
        '{OK}': ("{OK}", 'thumbs-up.png', 16, 16),
        '{X}': ("{X}", 'icon-error.png', 16, 16),
        '{i}': ("{i}", 'icon-info.png', 16, 16),
        '{1}': ("{1}", 'prio1.png', 15, 13),
        '{2}': ("{2}", 'prio2.png', 15, 13),
        '{3}': ("{3}", 'prio3.png', 15, 13),
        '{*}': ("{*}", 'star_on.png', 16, 16),
        '{o}': ("{o}", 'star_off.png', 16, 16),
    }
    del _

    def header(self, d, **kw):
        """ Assemble wiki header

        @param d: parameter dictionary
        @rtype: unicode
        @return: page header html
        """
        html = [
            # Pre header custom html
            self.emit_custom_html(self.cfg.page_header1),

            # Header
            u'<div id="header">',
            self.searchform(d),
            self.logo(),
            self.username(d),
            u'<h1 id="locationline">',
            self.interwiki(d),
            self.title_with_separators(d),
            u'</h1>',
            self.trail(d),
            self.navibar(d),
            # u'<hr id="pageline">',
            u'<div id="pageline"><hr style="display:none;"></div>',
            self.msg(d),
            self.editbar(d),
            u'</div>',

            # Post header custom html (not recommended)
            self.emit_custom_html(self.cfg.page_header2),

            # Start of page
            self.startPage(),
        ]
        return u'\n'.join(html)

    def editorheader(self, d, **kw):
        """ Assemble wiki header for editor

        @param d: parameter dictionary
        @rtype: unicode
        @return: page header html
        """
        html = [
            # Pre header custom html
            self.emit_custom_html(self.cfg.page_header1),

            # Header
            u'<div id="header">',
            u'<h1 id="locationline">',
            self.title_with_separators(d),
            u'</h1>',
            self.msg(d),
            u'</div>',

            # Post header custom html (not recommended)
            self.emit_custom_html(self.cfg.page_header2),

            # Start of page
            self.startPage(),
        ]
        return u'\n'.join(html)

    def footer(self, d, **keywords):
        """ Assemble wiki footer

        @param d: parameter dictionary
        @keyword ...:...
        @rtype: unicode
        @return: page footer html
        """
        page = d['page']
        html = [
            # End of page
            self.pageinfo(page),
            self.endPage(),

            # Pre footer custom html (not recommended!)
            self.emit_custom_html(self.cfg.page_footer1),

            # Footer
            u'<div id="footer">',
            self.editbar(d),
            self.credits(d),
            self.showversion(d, **keywords),
            u'</div>',

            # Post footer custom html
            self.emit_custom_html(self.cfg.page_footer2),
        ]
        return u'\n'.join(html)

    def username(self, d):
        """ Assemble the username / userprefs link

        @param d: parameter dictionary
        @rtype: unicode
        @return: username html
        """
        request = self.request
        _ = request.getText

        userlinks = []
        # Add username/homepage link for registered users. We don't care
        # if it exists, the user can create it.
        if request.user.valid and request.user.name:
            interwiki = wikiutil.getInterwikiHomePage(request)
            name = request.user.name
            aliasname = request.user.aliasname
            if not aliasname:
                aliasname = name
            title = "%s @ %s" % (aliasname, interwiki[0])
            # link to (interwiki) user homepage
            homelink = (
                request.formatter.interwikilink(1,
                                                title=title,
                                                id="userhome",
                                                generated=True,
                                                *interwiki) +
                request.formatter.text(name) + request.formatter.interwikilink(
                    0, title=title, id="userhome",
                    *interwiki))
            userlinks.append(homelink)
            # link to userprefs action
            if 'userprefs' not in self.request.cfg.actions_excluded:
                userlinks.append(d['page'].link_to(request,
                                                   text=_('Settings'),
                                                   querystr={'action':
                                                             'userprefs'},
                                                   id='userprefs',
                                                   rel='nofollow'))

        # comment out to remove login link
        if request.user.valid:
            if request.user.auth_method in request.cfg.auth_can_logout:
                userlinks.append(d['page'].link_to(
                    request,
                    text=_('Logout'),
                    querystr={'action': 'logout',
                              'logout': 'logout'},
                    id='logout',
                    rel='nofollow'))
        else:
            query = {'action': 'login'}
            # special direct-login link if the auth methods want no input
            if request.cfg.auth_login_inputs == ['special_no_input']:
                query['login'] = '1'
            if request.cfg.auth_have_login:
                userlinks.append(d['page'].link_to(request,
                                                   text=_("Login"),
                                                   querystr=query,
                                                   id='login',
                                                   rel='nofollow'))

        userlinks_html = u'<span class="sep"> | </span>'.join(userlinks)
        html = u'<div id="username">%s</div>' % userlinks_html
        return html

    def trail(self, d):
        """ Assemble page trail

        @param d: parameter dictionary
        @rtype: unicode
        @return: trail html
        """
        request = self.request
        user = request.user
        html = ''
        if not user.valid or user.show_page_trail:
            trail = user.getTrail()
            if trail:
                items = []
                for pagename in trail:
                    try:
                        interwiki, page = wikiutil.split_interwiki(pagename)
                        if interwiki != request.cfg.interwikiname \
                           and interwiki != 'Self':
                            link = (self.request.formatter.interwikilink(
                                True, interwiki, page) +
                                    self.shortenPagename(page) +
                                    self.request.formatter.interwikilink(
                                        False, interwiki, page))
                            items.append(link)
                            continue
                        else:
                            pagename = page

                    except ValueError:
                        pass
                    page = Page(request, pagename)
                    title = page.split_title()
                    title = self.shortenPagename(title)
                    link = page.link_to(request, title)
                    items.append(link)
                html = (u'<div id="pagetrail">%s</div>' %
                        u'<span class="sep"> &raquo; </span>'.join(items))
        return html

    def interwiki(self, d):
        """ Assemble the interwiki name display, linking to page_front_page

        @param d: parameter dictionary
        @rtype: string
        @return: interwiki html
        """
        if self.request.cfg.show_interwiki:
            page = wikiutil.getFrontPage(self.request)
            text = self.request.cfg.interwikiname or 'Self'
            link = page.link_to(self.request, text=text, rel='nofollow')
            html = u'<span id="interwiki">%s<span class="sep">: </span></span>' % link
        else:
            html = u''
        return html

    def actionsMenu(self, page):
        """Create actions menu list and items data dict

        The menu will contain the same items always, but items that are
        not available will be disabled (some broken browsers will let
        you select disabled options though).

        The menu should give best user experience for javascript
        enabled browsers, and acceptable behavior for those who prefer
        not to use Javascript.

        TODO: Move actionsMenuInit() into body onload - requires that
              the theme will render body, it is currently done in
              wikiutil/page.

        NH: Adapted from method in MoinMoin/theme/__init__.py

        @param page: current page, Page object
        @rtype: unicode
        @return: actions menu html fragment

        """
        request = self.request
        _ = request.getText
        rev = request.rev

        menu = [
            'raw',
            'print',
            'RenderAsDocbook',
            'refresh',
            '__separator__',
            'SpellCheck',
            'LikePages',
            'LocalSiteMap',
            '__separator__',
            'RenamePage',
            'CopyPage',
            'DeletePage',
            # '__separator__',
            # 'MyPages',
            # 'SubscribeUser',
            # '__separator__',
            # 'Despam',
            'revert',
            # 'PackagePages',
            # 'SyncPages',
            ]

        titles = {
            # action: menu title
            '__title__': _("More Actions:"),
            # Translation may need longer or shorter separator
            '__separator__': _('------------------------'),
            'raw': _('Raw Text'),
            'print': _('Print View'),
            'refresh': _('Delete Cache'),
            'SpellCheck': _('Check Spelling'),  # rename action!
            'RenamePage': _('Rename Page'),
            'CopyPage': _('Copy Page'),
            'DeletePage': _('Delete Page'),
            'LikePages': _('Like Pages'),
            'LocalSiteMap': _('Local Site Map'),
            'MyPages': _('My Pages'),
            'SubscribeUser': _('Subscribe User'),
            'Despam': _('Remove Spam'),
            'revert': _('Revert to this revision'),
            'PackagePages': _('Package Pages'),
            'RenderAsDocbook': _('Render as Docbook'),
            'SyncPages': _('Sync Pages'),
            }

        extra_titles = {
            'LMDigitalSignature': _('Document review (electronic signature)'),
            'LMRecordTraining': _('I have read this page...'),
            'LMShowTrainingStatus': _('Who has read this page?')
            }

        options = []
        option = '<option value="%(action)s"%(disabled)s>%(title)s</option>'
        # class="disabled" is a workaround for browsers that ignore
        # "disabled", e.g IE, Safari
        # for XHTML: data['disabled'] = ' disabled="disabled"'
        disabled = ' disabled class="disabled"'

        # Format standard actions
        available = get_available_actions(request.cfg, page, request.user)
        for action in menu:
            data = {'action': action, 'disabled': '', 'title': titles[action]}
            # removes excluded actions from the more actions menu
            if action in request.cfg.actions_excluded:
                continue

            # Enable delete cache only if page can use caching
            if action == 'refresh':
                if not page.canUseCache():
                    data['action'] = 'show'
                    data['disabled'] = disabled

            # revert action enabled only if user can revert
            if action == 'revert' and not request.user.may.revert(page.page_name):
                data['action'] = 'show'
                data['disabled'] = disabled

            # SubscribeUser action enabled only if user has admin rights
            if action == 'SubscribeUser' and not request.user.may.admin(page.page_name):
                data['action'] = 'show'
                data['disabled'] = disabled

            # PackagePages action only if user has write rights
            if action == 'PackagePages' and not request.user.may.write(page.page_name):
                data['action'] = 'show'
                data['disabled'] = disabled

            # Despam action enabled only for superusers
            if action == 'Despam' and not request.user.isSuperUser():
                data['action'] = 'show'
                data['disabled'] = disabled

            # Special menu items. Without javascript, executing will
            # just return to the page.
            if action.startswith('__'):
                data['action'] = 'show'

            # Actions which are not available for this wiki, user or page
            if (action == '__separator__' or
                (action[0].isupper() and not action in available)):
                data['disabled'] = disabled

            options.append(option % data)

        # Add custom actions not in the standard menu, except for
        # some actions like AttachFile (we have them on top level)
        more = [item for item in available
                if item not in titles and item not in ('AttachFile', )]
        more.sort()
        if more:
            # Add separator
            separator = option % {'action': 'show', 'disabled': disabled,
                                  'title': titles['__separator__']}
            options.append(separator)
            # Add more actions (all enabled)
            for action in more:
                data = {'action': action, 'disabled': ''}
                # Always add spaces: AttachFile -> Attach File
                # XXX do not create page just for using split_title -
                # creating pages for non-existent does 2 storage lookups
                # title = Page(request, action).split_title(force=1)

                # title = action
                # use title defined in extra_titles if available (NH)
                title = extra_titles.get(action, action)

                # Use translated version if available
                data['title'] = _(title)

                # LMDigitalSignature action only if user has write rights
                if action == 'LMDigitalSignature' \
                   and not request.user.may.write(page.page_name):
                    data['action'] = 'show'
                    data['disabled'] = disabled

                options.append(option % data)

        data = {
            'label': titles['__title__'],
            'options': '\n'.join(options),
            'rev_field': rev and ('<input type="hidden" name="rev" value="%d">' %
                                  rev or ''),
            'do_button': _("Do"),
            'baseurl': self.request.getScriptname(),
            'pagename_quoted': wikiutil.quoteWikinameURL(page.page_name),
            }
        html = '''
<form class="actionsmenu" method="GET" action="%(baseurl)s/%(pagename_quoted)s">
<div>
    <label>%(label)s</label>
    <select name="action"
        onchange="if ((this.selectedIndex != 0) &&
                      (this.options[this.selectedIndex].disabled == false)) {
                this.form.submit();
            }
            this.selectedIndex = 0;">
        %(options)s
    </select>
    <input type="submit" value="%(do_button)s">
    %(rev_field)s
</div>
<script type="text/javascript">
<!--// Init menu
actionsMenuInit('%(label)s');
//-->
</script>
</form>
''' % data

        return html


def execute(request):
    """
    Generate and return a theme object

    @param request: the request object
    @rtype: MoinTheme
    @return: Theme object
    """
    return Theme(request)
