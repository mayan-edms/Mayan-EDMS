###############
Troubleshooting
###############


********
Database
********

_mysql_exceptions. OperationalError: (1267, "Illegal mix of collations (latin1_swedish_ci, IMPLICIT) and (utf8_general_ci, COERCIBLE) for operation ‘='”)
=========================================================================================================================================================

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
=============================================================================

When using MySQL and doing OCR on languages other than English

Use utf-8 collation on MySQL server, or at least in table
‘documents_documentpage', ‘content' field

References:

* http://groups.google.com/group/django-users/browse_thread/thread/429447086fca6412
* http://markmail.org/message/bqajx2utvmtriixi


Error "django.db.utils.IntegrityError IntegrityError: (1452, ‘Cannot add or update a child row: a foreign key constraint fails (`…`.`…`, CONSTRAINT `…_refs_id_b0252274` FOREIGN KEY (`…`) REFERENCES `…` (`…`))')
==================================================================================================================================================================================================================

Solution:
Convert all MySQL tables to the same type, either all MyISAM or InnoDB


******
Docker
******

MAYAN_APT_INSTALLS does not work for Archlinux with kernels > 4.14
==================================================================

This is caused by a change from kernel 4.18 - 4.19. Metacopy on these kernels
is set to yes in archlinux kernels (/sys/module/overlay/parameters/metacopy)
and overlayfs should override this which it does not at the moment.

The workaround is to disable metacopy::

    echo N | sudo tee /sys/module/overlay/parameters/metacopy

References:

* https://bbs.archlinux.org/viewtopic.php?id=241866
* https://www.spinics.net/lists/linux-unionfs/msg06316.html



*********
Passwords
*********

Missing initial credentials or admin password reset
===================================================

First you need to know the name of the Docker container running Mayan EDMS
on your setup with::

    docker ps

Then execute the password reset command inside the Docker container::

    docker exec -ti <your docker container name> /bin/bash
    /opt/mayan-edms/bin/mayan-edms.py changepassword admin
