###
FAQ
###

*************
Non technical
*************

Distribution
============

Can I distribute Mayan EDMS under another name and/or logo?
-----------------------------------------------------------

Yes, the terms of the license allow this. However, the copyright notice must
remain intact. If you use an alternate name, a notice indicating that yours is
a derived product from Mayan EDMS must be included. You must indicate to your
clients that their act of purchasing Mayan EDMS from you is an independent
action and in no way legally binds Mayan EDMS LLC, the Mayan EDMS copyright
holders, or the core team in any way.


Sale
====

Can I sell Mayan EDMS as is or under another name?
--------------------------------------------------

Yes, selling Mayan EDMS is permitted. However, the copyright notice must
remain intact. If you use an alternate name, a notice indicating that yours is
a derived product from Mayan EDMS must be included. You must indicate to your
clients that their act of purchasing Mayan EDMS from you is an independent
action and in no way legally binds Mayan EDMS LLC, the Mayan EDMS copyright
holder, or the core team in any way. Note that when you sell Mayan EDMS,
you are selling your service and not a license, rights, or privileges of any
type.


Can I get exclusive distribution rights for my region?
------------------------------------------------------

No, the terms of the license make the project freely available to everyone.
Restricting distribution or sale would conflict with the license terms. This
would possible for a commercial version of Mayan EDMS with separate licensing
terms.

Is there a commercial partnership program?
------------------------------------------

There was at one time but was retired. If there is interest it could be
reinstated in the future.


What is an EDMS?
----------------

EDMS stands for Electronic Document Management System and it is an more modern
version of a DMS. A DMS is a Document Management System. A system to store,
sort, and categorize printed documents. It is an electronic filing system.
Besides images of scanned documents, an EDMS also support electronic documents,
documents created in a computer that may or may not have been printed.
While they may look similar, EDMS/DMS is not to be confused with CMS
(Content Management System), IM (Information Management), KM
(Knowledge Management), RM (Record management), ECM (Enterprise Content
Management). Mayan EDMS started initially as a strict EDMS project but has
been expanding its feature set and provide some functionality from other
system types.

*********
Technical
*********

Database managers
=================

PostgreSQL vs. MySQL
--------------------

Since Django abstracts database operations from a functional point of view
Mayan EDMS will behave exactly the same either way. The only concern would be
that MySQL doesn't support transactions for schema modifying commands. The only
moment this could cause problems is when running South migrations during
upgrades, if a migration fails the database structure is left in a transitory
state and has to be reverted manually before trying again.

_mysql_exceptions. OperationalError: (1267, "Illegal mix of collations (latin1_swedish_ci, IMPLICIT) and (utf8_general_ci, COERCIBLE) for operation ‘='”)
---------------------------------------------------------------------------------------------------------------------------------------------------------

::

    $ mayan-edms.py shell
    >>> from django.db import connection
    >>> cursor = connection.cursor()
    >>> cursor.execute('SHOW TABLES')
    >>> results=[]
    >>> for row in cursor.fetchall(): results.append(row)
    >>> for row in results: cursor.execute('ALTER TABLE %s CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;' % (row[0]))

References:

* http://stackoverflow.com/questions/1073295/django-character-set-with-mysql-weirdness


Incorrect string value: ``'xE2x80x95rs6…'`` for column ``'content'`` at row 1
-----------------------------------------------------------------------------

When using MySQL and doing OCR on languages other than English

Use utf-8 collation on MySQL server, or at least in table
‘documents_documentpage', ‘content' field

References:

* http://groups.google.com/group/django-users/browse_thread/thread/429447086fca6412
* http://markmail.org/message/bqajx2utvmtriixi

Error "django.db.utils.IntegrityError IntegrityError: (1452, ‘Cannot add or update a child row: a foreign key constraint fails (`…`.`…`, CONSTRAINT `…_refs_id_b0252274` FOREIGN KEY (`…`) REFERENCES `…` (`…`))')
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Solution:
Convert all MySQL tables to the same type, either all MyISAM or InnoDB


Document versions
=================

How do you upload a new version of an existing file?
----------------------------------------------------

Choose a document, and go to the versions tab, on the right menu at the bottom
under Other available action there is Upload new version. Clicking it will
take you to a very similar view as the Upload new document but you will be
able to specify version number and comments for the new version being uploaded.

LDAP
====

How to do LDAP authentication
-----------------------------

A sample settings file called ldap_connection_settings.py is included in the
contrib/settings/ folder of the repository showing how to setup LDAP
authentication.

Operating systems
=================

How to install Mayan EDMS in Windows operating systems?
-------------------------------------------------------

Mayan EDMS doesn't run natively on Windows. The best way is to use a virtual
machine product, install Ubuntu or Debian, and proceed with the standard
deployment instructions or use Docker inside a GNU/Linux virtual machine.


Python
======

Is virtualenv required as specified in the documentation?
---------------------------------------------------------

It is not necessary, but it's a strong recommendation mainly to reduce
dependency conflicts by isolation from the main Python system install. If not
using a virtualenv, pip would install Mayan's dependencies globally coming in
conflict with the distribution's prepackaged Python libraries messing other
Django projects or Python programs, or another later Python/Django project
dependencies coming into conflict causing Mayan to stop working for no
apparent reason.


Does Mayan EDMS work with Python 3?
-----------------------------------

Yes but it is not production ready yet. Users are encouraged to deploy test
installations of Mayan EDMS on Python 3 and report findings.


Static files
============

Mayan EDMS installed correctly and works, but static files are not served
-------------------------------------------------------------------------

Django's development server doesn't serve static files unless the DEBUG option
is set to True, this mode of operation should only be used for development or
testing. For production deployments the management command::

    $ mayan-edms.py collectstatic

should be used and the resulting static folder served from a webserver.
For more information check the
:django-docs:`howto/static-files/`

Watchfolders
============

The watched folder feature is not working
-----------------------------------------

Make sure that the Celery BEAT scheduler is running correctly as it is the
element that triggers the periodics tasks.

Other
=====

File system links not showing when serving content with ``Samba``
-----------------------------------------------------------------

Disable unix extensions in the [global] section and enable wide links for the file serving share

Example::

    [global]
        unix extensions = no

        ...

    [digitalizacion]
        path = /var/local/mayan
        guest ok = yes
        read only = yes
        wide links = yes
        follow symlinks = yes


Reference:
* http://www.samba.org/samba/docs/man/manpages-3/smb.conf.5.html

Can you change the display order of documents…i.e can they be in alphabetical order?
------------------------------------------------------------------------------------

A the moment no, but it is something being worked on.
