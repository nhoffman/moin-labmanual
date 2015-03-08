======
moinlm
======

Lab Med implementation and customization of the MoinMoin wiki::

   $Id$

.. contents::

About this document
===================

This is a reStructuredText document which has a relateively simple markup
language. Go to this link for a quick reference.

    http://docutils.sourceforge.net/docs/user/rst/quickref.html


Dependencies
============

 * Python 2.5+
 * MoinMoin 1.8.4+ (http://moinmo.in/)
 * docutils (http://docutils.sourceforge.net/) to compile reStructured text documentation

Project contents
================

The mapping between contents of this repository and the
system-level MoinMoin instance is partially explained in ./setenv.sh:

.. include:: setenv.sh
   :literal:

The project has the following directory hierarchy (description or mapping to the system
file is shown where applicable)::

  moinlm
  |-- Makefile
  |-- README.html
  |-- README.txt
  |-- __init__.py
  |-- config/         --> $INSTANCE/config
  |-- htdocs/         --> $HTML/htdocs
  |-- instance/       (templates for new wikis)
  |-- misc/           (misc files to support package development)
  |-- notes.txt
  |-- plugin/         --> $INSTANCE/<each wiki>/data/plugin
  |-- scripts/        (scripts for installation, etc)
  |-- setenv.sh       (defines system location for installation of new wiki)
  |-- setup.py
  `-- tests/          --> unit tests (barely implemented)

The contents of the plugin directory contain MoinMoin extensions and are installed
in the plugin directory for each wiki in the wikifarm::

  plugin
  |-- action/
  |   |-- CreatePdfDocument.py
  |   |-- LMRecordTraining.py
  |   |-- LMShowTrainingStatus.py
  |   `-- lmWriteTrainingLog.py
  |-- converter/
  |-- filter/
  |-- formatter/
  |-- macro/
  |   |-- LMDraftWarning.py
  |   |-- LMLastEdited.py
  |   |-- LMPageBreak.py
  |   |-- LMPageList.py
  |   |-- LMSystemInfo.py
  |   |-- LMTestMacro.py
  |   |-- LMUserInfo.py
  |   `-- LMWarningBox.py
  |-- parser/
  |-- theme/
  |   |-- __init__.py
  |   |-- modern_cms_lm.py
  |   |-- modernized_cms_lm.py
  |   |-- modernized_lm.py
  |   `-- rightsidebar_cms_lm.py
  `-- xmlrpc/

MoinMoin docs
=============

Relevant MoinMoin help pages (add 'em as you find 'em):

 * http://moinmo.in/HelpOnInstalling/BasicInstallation
 * http://moinmo.in/HelpOnInstalling/WikiInstanceCreation
 * http://moinmo.in/HelpOnInstalling/ApacheOnLinux

Development
===========

This project was designed to support development in a user-owned
location under version control; changes are copied to a system
location on execution of a script. Please do *not* modify files in the
system location, because changes will be clobbered!

After making local changes, copy files to the system location using
scripts executed from the Makefile::

  $ cd moinlm
  $ make install -n
  /usr/local/bin/python setup.py install
  /usr/local/bin/python scripts/install_plugin.py /var/www/html/moinlm /var/www/html/htdocs
  source setenv.sh; scripts/update_permissions.sh
  $ sudo make install
  
Create a new wiki
=================

A new wiki may be added to the wikifarm programmatically::

  $ make new WIKINAME=mynewwiki -n
  source setenv.sh; export WIKINAME=mynewwiki; scripts/add_wiki.sh
  $ sudo make new WIKINAME=mynewwiki

Complete the installation of the wiki (transfers files created locally
into the system location)::

  sudo make install

 Add the new wiki config file to the svn repository::

  svn add config/*.py

And some additional apache-related steps:

 * add an .htaccess file to $WIKILOCATION/mynewwiki
 * Create a ScriptAlias to the new wiki in httpd.conf (this is 
   found in /etc/httpd/conf/httpd.conf on RHEL)::

    ScriptAlias /mynewwiki "/var/www/html/mynewwiki/moin.cgi"


Backups and archives
====================

Both archives and backups are written to a shared file system on lilith. This
was mounted to /mnt/webbackup from web.labmed.washington.edu. The host lilith
is backed on tape which is transported off site.

Archive
~~~~~~~

A archive is created for all wikis using scripts/moin-create-archives via a
root crontab. Actually the crontab runs a copy of that script located in
/root. So if changes are made, be sure to update the copy in /root. This script
is run daily and the archive is stored in the /mnt/webbackup/moin/archives
directory. The individual archives can be extracted using either the ZIP file,
or the self-extracting EXE file for windows. To bring up the archive after
extracting the files, point your browser to the index.html file. Note that only
the latest snapshot of the wikis is stored on disk.

Backup
~~~~~~

Backups for the entire wiki site are performed using scripts/moin-backup. As
with the archive, the crontab which activates the backup refers to a copy of
this script located in /root. The backup files are stored in the
/mnt/webbackup/moin/backups directory in a 5 day rotation (M-F).


Access Control
==============

Access control is separated into two areas: control of access to the web site,
and control of access to individual wiki pages. This section desribes
everything you want to know about these two topics.

Web site access
~~~~~~~~~~~~~~~

Access to the wiki web site is controlled by the ``.htaccess`` file you set up in the
`Create a new wiki`_ section. This file exists primarily to specify which
groups of people are allowed access to the web site. A typical ``.htaccess``
file looks like this::

    AuthType UWNetID
    AuthGroupFile /etc/httpd/.htgroup
    PubcookieAppID "labmanual"
    require group admin residents faculty supervisors fellows

The first line says that authentication is done using the UWNetID. This is why
you need to login on MyUW. The second line says where the ``.htgroup`` file is
located. It is not clear that the full pathname is required, but it is probably
a good practice to do so. This way there is no confusion about which
``.htgroup`` file is being used.  More on the ``.htgroup`` file later. The
third line specifies part of the name of the cookie associated with this
wiki. When you create a wiki, it is easiest to just specify the name of the
wiki here. If you use Firefox, you can see the cookie by doing Tools -> Options
-> Privacy -> remove individual cookies. Then scroll down to
web.labmed.washington.edu and open up the list. The result looks like this:

.. image:: images/cookie-dialog.jpg

The fourth line of the sample ``.htaccess`` file indicates which groups in the
``.htgroup`` file are allowed.

On web.labmed.washington.edu the ``.htgroup`` file is located in ``/etc/httpd/.htgroup``
The ``.htgroup`` file contains lines of the following form: a group name, followed by a
colon (:), followed by a list of UWNetIDs that are members of that group. The
space character is used to separate UWNetIDs. For example::

    fellows: agger001 anabbott fstrath mroshal plattebo succeed tamukele

The web site:

    https://depts.washington.edu/labmed1/admin/

can be used to manage the ``.htgroup`` file. Using this to manage ``.htaccess``
files may not work. At some point in the future, this link may be changed to
allow one to manage ``.htgroup`` and ``.htaccess`` files. The script
``/home/ctaff/get_htgroup.sh`` is run as a cron job every day to transfer the
.htgroup file from the upper campus to web.labmed.washington.edu. Because of
this, it it not a good idea to edit the ``.htgroup`` manually on
web.labmed.washington.edu because it will get overwritten. The actual file is
located on ovid.u.washington.edu in ``~labmed1/public_html/.htgroup``.


Wiki page access
~~~~~~~~~~~~~~~~

Access to wiki files follows an access control list approach. Overall access is
controlled in the wiki's Python file located in the config directory. For the
labmanual wiki this is located in config/labmanual.py. The last few lines of
that file are::

    acl_rights_default = u"AdminGroup:admin,read,write,delete,revert"
    acl_rights_default += u" LabMedEditorsGroup:read,write,delete,revert"
    acl_rights_default += u" LabMedFacultyGroup:read,write"
    acl_rights_default += u" LabMedLeadsGroup:read,write"
    acl_rights_default += u" LabMedSupervisorsGroup:read,write"
    acl_rights_default += u" LabMedClinTechTwoGroup:read,write"
    acl_rights_default += u" LabMedCompStaffGroup:read,write"
    acl_rights_default += u" LabMedResidentsGroup:read,write"
    acl_rights_default += u" LabMedFellowsGroup:read,write"
    acl_rights_default += u" LabMedSpsGroup:read,write"
    acl_rights_default += u" All:read"

This defines access for each wiki group (this is not the same as the groups in the
previous section). More details on this can be found here:

    http://moinmo.in/4ct10n/show/HelpOnAccessControlLists

There are some predefined wiki groups, like AdminGroup and All, and the rest
are user-defined. When access is not defined, the list in tne wiki's Python
file is used by defaullt.

When one wants to control access to a wiki page, one puts a line like the
following as the first line of the page::

    #acl AdminGroup:admin,read,write All:read

This example allows members of the AdminGroup admin, read and write access.
The members of the user-defined groups, and all others, are only given read
access.

The group definitions can be found by navigating from the wiki home ->
GroupDefinitions. A group definition file specifies which UWNetIDs are
members of that group. The ordering of the list is specified in the wiki's
Python file, not the ordering you see on the GroupDefinitions page.
The following is the GroupDefinitions page for labmanual:

.. image:: images/group-definitions.jpg

If you are having trouble with the access you see on a new wiki, you may want
to remove the dictionary file. For the labmanual wiki, the dictionary file is:

    /var/www/html/moinlm/labmanual/data/cache/labmanual/wikidicts/dicts_groups

After editing a group definitions file, the dictionary file is automatically
updated.


TODO: update for web and further document

Development notes
=================

Please add to moinlm/notes.txt
