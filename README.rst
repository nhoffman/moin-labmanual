======
moinlm
======

Use MoinMoin as a CMS for document control in the clinical laboratory

Dependencies
============

* Python 2.7
* MoinMoin 1.9.8 (http://moinmo.in/)

Running in standalone mode
==========================

"Standalone mode" (running MoinMoin on your local machine using the
built-in webserver) is a good way to evaluate and develop these plugin
modules. Here's a step-by-step guide.

Execute the setup script ``dev/setup_standalone.sh`` to perform the
following actions:

* download and unpack the MoinMoin tarball to ``./src/``
* create a virtualenv ``./moin-env``
* install MoinMoin to the virtualenv
* create ``./wiki`` containing data for the wiki instance (copied from
  the MoinMoin package)
* create a test user "testuser" with password "testpass"

After executing the above script, activate the virtualenv and start
the standalone server::

  source moin-env/bin/activate
  ./wikiserver.py

At this point you can open your browser and point it to
http://localhost:8080 - but there isn't much to see until we install
the "underlay", containing system and help pages. To do so, log in
using the user name and password above. After logging in, go to this
url:

http://localhost:8080/LanguageSetup?action=language_setup&target=English--all_pages.zip&language=English

You should see the message "Attachment 'English--all_pages.zip' installed"

Finally, restart the server by interrupting the ``wikiserver.py`` script
(press control+C), then starting it again. At this point the tabs
("RecentChanges", "FindPage") should have content.
