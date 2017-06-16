===
FAQ
===

Frequently asked questions and solutions

**Q: PostgreSQL vs. MySQL**

Since Django abstracts database operations from a functional point of view
Mayan EDMS will behave exactly the same either way.  The only concern
would be that MySQL doesn't support transactions for schema modifying
commands. The only moment this could cause problems is when running
South migrations during upgrades, if a migration fails the database
structure is left in a transitory state and has to be reverted manually
before trying again.


**Q: _mysql_exceptions. OperationalError: (1267, "Illegal mix of collations (latin1_swedish_ci, IMPLICIT) and (utf8_general_ci, COERCIBLE) for operation '='")**

* Solution::

  $ mayan-edms.py shell

  >>> from django.db import connection
  >>> cursor = connection.cursor()
  >>> cursor.execute('SHOW TABLES')
  >>> results=[]
  >>> for row in cursor.fetchall(): results.append(row)
  >>> for row in results: cursor.execute('ALTER TABLE %s CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;' % (row[0]))


* References:

  - http://www.djangoshmango.com/?p=99
  - http://stackoverflow.com/questions/1073295/django-character-set-with-mysql-weirdness


**Q: Incorrect string value: ``'\xE2\x80\x95rs6...'`` for column ``'content'`` at row 1**

When using ``MySQL`` and doing OCR on languages other than English

* Solution:

  - Use utf-8 collation on MySQL server, or at least in table 'documents_documentpage', 'content' field
  - Ref: 1- http://groups.google.com/group/django-users/browse_thread/thread/429447086fca6412
  - Ref: 2- http://markmail.org/message/bqajx2utvmtriixi


**Q: Error "django.db.utils.IntegrityError IntegrityError: (1452, 'Cannot add or update a child row: a foreign key constraint fails (`...`.`...`, CONSTRAINT `..._refs_id_b0252274` FOREIGN KEY (`...`) REFERENCES `...` (`...`))')**

* Solution:

  - Convert all MySQL tables to the same type, either all MyISAM or InnoDB


**Q: File system links not showing when serving content with ``Samba``**

* Solution:

  - Disable unix extensions in the [global] section and enable wide links for the file serving share
  - Example::

      [global]
          unix extensions = no

          ...

      [digitalizacion]
          path = /var/local/mayan
          guest ok = yes
          read only = yes
          wide links = yes
          follow symlinks = yes


  - Ref: 1- http://www.samba.org/samba/docs/man/manpages-3/smb.conf.5.html


**Q: How do you upload a new version of an existing file?**

* Solution:

  - Choose a document, and go to the versions tab, on the right menu at
    the bottom under ``Other available action`` there is
    ``Upload new version``.  Clicking it will take you to a very similar
    view as the ``Upload new document`` but you will be able to specify
    version number and comments for the new version being uploaded.



**Q: Is virtualenv required as specified in the documentation?**

* It is not necessary, but it's a strong recommendation mainly to reduce
  dependency conflicts by isolation from the main Python system install.
  If not using a virtualenv, pip would install Mayan's dependencies
  globally coming in conflict with the distribution's prepackaged Python
  libraries messing other Django projects or Python programs, or another
  later Python/Django project dependencies coming into conflict causing
  Mayan to stop working for no apparent reason.


**Q: Mayan EDMS installed correctly and works, but static files are not served**

Django's development server doesn't serve static files unless the ``DEBUG``
option is set to ``True``, this mode of operation should only be used for
development or testing.  For production deployments the management command::

  $ mayan-edms.py collectstatic

should be used and the resulting ``static`` folder served from a webserver.
For more information, read https://docs.djangoproject.com/en/dev/howto/static-files/
and https://docs.djangoproject.com/en/1.2/howto/static-files/ or
http://mayan-edms-ru.blogspot.com/2011/11/blog-post_09.html


**Q:  Can you change the display order of documents...i.e can they be in alphabetical order?**

A the moment no, but it is something being considered.

**Q: Does Mayan EDMS work with Python 3?**

Not at the moment. When all the projects and libraries upon which Mayan is
dependent support Python 3 then will the project move to fully support Python 3.

**Q: The watched folder feature is not working**

Make sure that the Celery BEAT scheduler is running correctly as it is the element
that triggers the periodics tasks.

**Q: How to do LDAP authentication**

A sample settings file called ldap_connection_settings.py is included in the
contrib/settings/ folder of the repository showing how to setup LDAP
authentication.

