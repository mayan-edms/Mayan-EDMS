===
FAQ
===

Frequently asked questions and solutions

Database related
----------------

**Q: PostgreSQL vs. MySQL**

Since Django abstracts database operations from a functional point of view
**Mayan EDMS** will behave exactly the same either way.  The only concern
would be that MySQL doesn't support transactions for schema modifying
commands.  The only moment this could cause problems is when running
South migrations during upgrades, if a migration fails the database
structure is left in a transitory state and has to be reverted manually
before trying again.


**Q: _mysql_exceptions. OperationalError: (1267, "Illegal mix of collations (latin1_swedish_ci, IMPLICIT) and (utf8_general_ci, COERCIBLE) for operation '='")**

* Solution::

  $ manage.py shell
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


Document sharing
----------------

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


Document handling
-----------------

**Q: How to enable the ``GridFS`` storage backend**

* Solution:
   
  - Add the following lines to ``settings.py``::

      from storage.backends.gridfsstorage import GridFSStorage
      DOCUMENTS_STORAGE_BACKEND = GridFSStorage
  - Filesystem metadata indexing will not work with this storage backend as
    the files are inside a ``MongoDB`` database and can't be linked (at least for now)

**Q: How do you upload a new version of an existing file?**

* Solution:

  - Choose a document, and go to the versions tab, on the right menu at
    the bottom under ``Other available action`` there is
    ``Upload new version``.  Clicking it will take you to a very similar
    view as the ``Upload new document`` but you will be able to specify
    version number and comments for the new version being uploaded.

**Q: Site search is slow**

* Add indexes to the following fields:
  
  - ``documents_document`` - description, recommended size: 160
  - ``documents_documentpage`` - content, recommended size: 3000
  
This is a temporary solution as **Mayan EDMS** will soon be moving to a
specialized full text search solution.


Webserver
---------

**Q: How to enable x-sendile support for ``Apache``**

* If using Ubuntu execute the following::
 
  $ sudo apt-get install libapache2-mod-xsendfile

* Add the following line to your ``settings.py`` file::
  
    SENDFILE_BACKEND = 'sendfile.backends.xsendfile'

* On your apache configuration file add::
  
    XSendFile on
    XSendFileAllowAbove on
      

Deployments
-----------

**Q: Is virtualenv required as specified in the documentation?**

* It is not necessary, it's just a strong recommendation mainly to reduce
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

  $ ./manage.py collectstatic
  
should be used and the resulting ``static`` folder served from a webserver.
For more information, read https://docs.djangoproject.com/en/dev/howto/static-files/
and https://docs.djangoproject.com/en/1.2/howto/static-files/ or 
http://mayan-edms-ru.blogspot.com/2011/11/blog-post_09.html 

  
Other
-----


**Q: How to connect Mayan EDMS to an Active Directory tree**

I used these two libraries as they seemed the most maintained from the quick search I did.

* http://www.python-ldap.org/
* http://packages.python.org/django-auth-ldap/

After figuring out the corresponding OU, CN and such (which took quite a while since I'm not well versed in LDAP).  For configuration options, Mayan EDMS imports settings_local.py after importing settings.py to allow users to override the defaults without modifying any file tracked by Git, this makes upgrading by using Git's pull command extremely easy.  My settings_local.py file is as follows:

::

    import ldap
    from django_auth_ldap.config import LDAPSearch

    # makes sure this works in Active Directory
    ldap.set_option(ldap.OPT_REFERRALS, 0)

    AUTH_LDAP_SERVER_URI = "ldap://172.16.XX.XX:389"
    AUTH_LDAP_BIND_DN = 'cn=Roberto Rosario Gonzalez,ou=Aguadilla,ou=XX,ou=XX,dc=XX,dc=XX,dc=XX'
    AUTH_LDAP_BIND_PASSWORD = 'XXXXXXXXXXXXXX'
    AUTH_LDAP_USER_SEARCH = LDAPSearch('dc=XX,dc=XX,dc=XX', ldap.SCOPE_SUBTREE, '(SAMAccountName=%(user)s)')

    # Populate the Django user from the LDAP directory.
    AUTH_LDAP_USER_ATTR_MAP = {
        "first_name": "givenName",
        "last_name": "sn",
        "email": "mail"
    }

    # This is the default, but I like to be explicit.
    AUTH_LDAP_ALWAYS_UPDATE_USER = True

    AUTHENTICATION_BACKENDS = (
        'django_auth_ldap.backend.LDAPBackend',
        'django.contrib.auth.backends.ModelBackend',
    )



if your organization policies don't allow anonymous directory queries,
create a dummy account and set the ``AUTH_LDAP_BIND_DN`` and
``AUTH_LDAP_BIND_PASSWORD`` options to match the account.

For a more advanced example check this StackOverflow question:
http://stackoverflow.com/questions/6493985/django-auth-ldap


**Q:  Can you change the display order of documents...i.e can they be in alphabetical order?**

A the moment no, but it is something being considered.


**Q:  How to set the default language and have users not be able to change it?

Add the following to ``settings_local.py``:::

    LANGUAGE_CODE = 'es'

    MIDDLEWARE_CLASSES = (
        
        -- Copy all the classes from MIDDLEWARE_CLASSES in ``settings.py`` except for 'django.middleware.locale.LocaleMiddleware'
        
    )
