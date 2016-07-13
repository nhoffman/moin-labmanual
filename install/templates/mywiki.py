# -*- coding: utf-8 -*-
# IMPORTANT! This encoding (charset) setting MUST be correct! If you live in a
# western country and you don't know that you use utf-8, you probably want to
# use iso-8859-1 (or some other iso charset). If you use utf-8 (a Unicode
# encoding) you MUST use: coding: utf-8
# That setting must match the encoding your editor uses when you modify the
# settings below. If it does not, special non-ASCII chars will be wrong.

"""
This is a sample config for a wiki that is part of a wiki farm and uses
farmconfig for common stuff. Here we define what has to be different from
the farm's common settings.
"""

from os import path

# we import the FarmConfig class for common defaults of our wikis:
from farmconfig import FarmConfig


# now we subclass that config (inherit from it) and change what's different:
class Config(FarmConfig):

    # basic options (you normally need to change these)
    sitename = u'MyWiki'  # [Unicode]
    interwikiname = u'MyWiki'  # [Unicode]

    # name of entry page / front page [Unicode], choose one of those:

    # a) if most wiki content is in a single language
    # page_front_page = u"MyStartingPage"

    # b) if wiki content is maintained in many languages
    page_front_page = u"FrontPage"

    navi_bar = [
        # If you want to show your page_front_page here:
        u'%(page_front_page)s',
        u'RecentChanges',
        u'FindPage',
        u'HelpContents',
    ]

    data_dir = '{{ DATA_DIR }}/{{ item }}/data/'

    # xapian setup, see https://moinmo.in/HowTo/UbuntuFarm
    # we're specifying the location here so that we can have a separate index per wiki
    xapian_index_dir = path.join(data_dir, 'cache', 'xapian')
