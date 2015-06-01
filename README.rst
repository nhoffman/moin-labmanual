======
moinlm
======

Use MoinMoin as a CMS for document control in the clinical laboratory

Dependencies
============

* Python 2.7
* MoinMoin 1.9.8 (http://moinmo.in/)

Features
========



Running in standalone mode
==========================

"Standalone mode" (running MoinMoin on your local machine using the
built-in webserver) is a good way to evaluate and develop these plugin
modules. Here's a step-by-step guide.

First, execute this script from within the project repository::

  dev/setup_standalone.sh

This script will perform the following actions:

* download and unpack the MoinMoin tarball to ``./src/``
* create a virtualenv ``./moin-env``
* install MoinMoin to the virtualenv
* create ``./wiki`` containing data for the wiki instance (copied from
  the MoinMoin package)
* create a test user "testuser" with password "testpass"
* create a MoinMoin "package" ``pages.zip`` attached to the page
  "LanguageSetup" for installation.

After executing the above script, activate the virtualenv and start
the standalone server::

  source moin-env/bin/activate
  ./wikiserver.py

At this point you can open your browser and point it to
http://localhost:8080 - but there isn't much to see until we install
the "underlay", containing system and help pages. To do so, log in
using the user name "testuser" and password "testpass". After logging
in, visit the following url in your browser:

http://localhost:8080/LanguageSetup?action=language_setup&target=English--all_pages.zip

You should see the message "Attachment 'English--all_pages.zip' installed"

Next, install the underlay pages for this project. Visit this url:

http://localhost:8080/LanguageSetup?action=AttachFile

and find the entry for '000-moin-labmanual.zip' (should be the first line
on the page), and click on "install".

Finally, restart the server by interrupting the ``wikiserver.py``
script (press control+C), then starting it again. At this point the
tabs ("RecentChanges", "FindPage", etc) should have content. The front
page of the wiki should now be "HelpOnLMMacros", which provides
documentation for macros provided in this package.

As configured above, the code in the ``moinlm`` package is imported
directly by ``wikiserver.py`` (ie, the package does not need to be
installed to the virtualenv), but changes to the code won't be
registered until the server is restarted. During development, it's
convenient to use ``dev/run_standalone.py`` to launch the server. This
is simply a wrapper that runs ``wikiserver.py`` and will perform a
restart after Ctrl-C.
