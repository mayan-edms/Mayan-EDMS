===
FAQ
===

Frequently asked questions and solutions



_mysql_exceptions.OperationalError: (1267, "Illegal mix of collations (latin1_swedish_ci,IMPLICIT) and (utf8_general_ci,COERCIBLE) for operation '='")
------------------------------------------------------------------------------------------------------------------------------------------------------

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
        
        
        
Incorrect string value: ``'\xE2\x80\x95rs6...'`` for column ``'content'`` at row 1
----------------------------------------------------------------------------------

When using ``MySQL`` and doing OCR on languages other than English
    
  * Solution:
  
    - Use utf-8 collation on MySQL server, or at least in table 'documents_documentpage', 'content' field
    - Ref: 1- http://groups.google.com/group/django-users/browse_thread/thread/429447086fca6412
    - Ref: 2- http://markmail.org/message/bqajx2utvmtriixi

File system links not showing when serving content with ``Samba``
-----------------------------------------------------------------

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


How to store documents outside of **Mayan EDMS's** path
-------------------------------------------------------

  * Sub class Django's ``FileSystemStorage`` class:
    
    - Create a file called ``customstorage.py``::
      
        from django.core.files.storage import FileSystemStorage

        class CustomStorage(FileSystemStorage):
            def __init__(self, *args, **kwargs):
                super(CustomStorage, self).__init__(*args, **kwargs)
                self.location='/new/path/to/documents/'
                self.base_url='document_storage'

    - In the ``settings.py`` add::
    
        from customstorage import CustomStorage
        DOCUMENTS_STORAGE_BACKEND = CustomStorage


How to enable the ``GridFS`` storage backend
--------------------------------------------

    * Solution:
    
      - Add the following lines to ``settings.py``::
      
          from storage.backends.gridfsstorage import GridFSStorage
          DOCUMENTS_STORAGE_BACKEND = GridFSStorage
        
      - Filesystem metadata indexing will not work with this storage backend as
        the files are inside a ``MongoDB`` database and can't be linked (at least for now)


Site search is slow
-------------------

  * Add indexes to the following fields:
  
    - ``documents_document`` - description, recommended size: 160
    - ``documents_documentmetadata`` - value, recommended size: 80
    - ``documents_documentpage`` - content, recommended size: 3000


How to enable x-sendile support for ``Apache``
----------------------------------------------

  * Add the following line to your ``settings.py`` file::
  
      SENDFILE_BACKEND = 'sendfile.backends.xsendfile'
    
  * On your apache configuration file add::
  
      XSendFile on
      XSendFileAllowAbove on
