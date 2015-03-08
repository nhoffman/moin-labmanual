# -*- coding: utf-8 -*-
"""
    MoinMoin - mod_wsgi driver script

    To use this, add those statements to your Apache's VirtualHost definition:

    # you will invoke your moin wiki at the root url, like http://servername/FrontPage:
    WSGIScriptAlias / /some/path/moin.wsgi

    # create some wsgi daemons - use someuser.somegroup same as your data_dir:
    WSGIDaemonProcess daemonname user=someuser group=somegroup processes=5 threads=10 maximum-requests=1000 umask=0007

    # use the daemons we defined above to process requests!
    WSGIProcessGroup daemonname

    @copyright: 2008 by MoinMoin:ThomasWaldmann
    @license: GNU GPL, see COPYING for details.
"""

import sys
import os
import site

# a) Configuration of Python's code search path
#    If you already have set up the PYTHONPATH environment variable for the
#    stuff you see below, you don't need to do a1) and a2).

# a1) Path of the directory where the MoinMoin code package is located.
#     Needed if you installed with --prefix=PREFIX or you didn't use setup.py.
#sys.path.insert(0, 'PREFIX/lib/python2.3/site-packages')

# Use virtualenv for this site
# see https://code.google.com/p/modwsgi/wiki/VirtualEnvironments
# Remember original sys.path.
prev_sys_path = list(sys.path)

# Add each new site-packages directory.
ALLDIRS = ['{{ VENV }}/lib/python2.7/site-packages']
for directory in ALLDIRS:
    site.addsitedir(directory)

# Reorder sys.path so new directories at the front.
new_sys_path = []
for item in list(sys.path):
    if item not in prev_sys_path:
        new_sys_path.append(item)
        sys.path.remove(item)
sys.path[:0] = new_sys_path

# a2) Path of the directory where wikiconfig.py / farmconfig.py is located.
#     See wiki/config/... for some sample config files.
sys.path.insert(0, '{{ DATA_DIR }}')
#sys.path.insert(0, '/path/to/farmconfigdir')

# b) Configuration of moin's logging
#    If you have set up MOINLOGGINGCONF environment variable, you don't need this!
#    You also don't need this if you are happy with the builtin defaults.
#    See wiki/config/logging/... for some sample config files.
#from MoinMoin import log
#log.load_config('/path/to/logging_configuration_file')

from MoinMoin.web.serving import make_application

# Creating the WSGI application
# use shared=True to have moin serve the builtin static docs
# use shared=False to not have moin serve static docs
# use shared='/my/path/to/htdocs' to serve static docs from that path
application = make_application(shared=True)
