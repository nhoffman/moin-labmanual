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

TODO: write me!


Running in standalone mode
==========================

"Standalone mode" (running MoinMoin on your local machine using the
built-in webserver) is a good way to evaluate and develop these plugin
modules. Here's a step-by-step guide.

First, execute this script from within the project repository::

  dev/setup_standalone.sh

This script will perform the following actions:

* download and unpack the MoinMoin tarball to ``./src/moin-1.9.8``
* create link ``wikiserver.py -> src/moin-1.9.8/wikiserver.py``
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
using the user name "superuser" and password "superpass". After logging
in, visit the following url in your browser:

http://localhost:8080/LanguageSetup?action=language_setup&target=English--all_pages.zip

You should see the message "Attachment 'English--all_pages.zip' installed"

Next, install the underlay pages for this project. Visit this url:

http://localhost:8080/LanguageSetup?action=language_setup&target=000-moinlm-pages.zip

You should see the message "Attachment '000-moinlm-pages.zip' installed"

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

importing live data
-------------------

It can be useful to test features in development by copying data from
a production instance of a wiki. This is fairly easily
accomplished. Let's say we have a wiki named ``compstaff`` hosted on a
server with ssh alias ``docs`` with ``data`` in
``/home/moinmoin/compstaff``. On the server::

  cd /home/moinmoin/compstaff
  tar -czf /tmp/compstaff.tgz data/pages

Now, locally::

  scp docs:/tmp/compstaff.tgz .
  tar -xf compstaff.tgz
  find data -name cache | xargs rm -r
  cp -r data/pages/* wiki/data/pages

Note that this method does not retrieve the edit log or user data.


Deploying a wiki farm
=====================

This project provides an ansible script for deploying a wiki
farm. Assuming you have already created a virtualenv, first, install
ansible::

  pip install ansible

Run the deployment script as follows::

  install/install-farm.yml -i install/hosts

After completion of this script, you will need to manually install the
underlay pages and help pages for the moinlm project more or less as
above. Log in using the superuser credentials (XXX define these
someplace), then visit your new site and append the following to the
base url::

  /LanguageSetup?action=language_setup&target=English--all_pages.zip

You should see the message "Attachment 'English--all_pages.zip' installed"

Next, install the underlay pages for this project. Visit this url::

  /LanguageSetup?action=AttachFile

and find the entry for '000-moinlm-pages.zip' (should be the first
line on the page), and click on "install". You will need to restart
apache for these changes to take effect::

  sudo service apache2 restart



