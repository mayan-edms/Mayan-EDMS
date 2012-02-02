============
File storage
============

The files are stored and placed under **Mayan EDMS** "control" to avoid
filename clashes (each file gets renamed to its UUID and with an extension)
and stored in a simple flat arrangement in a directory.  This doesn't
stop access to the files but it is not recommended because moving,
renaming or updating the files directly would throw the database out
of sync.  For access to the files the recommended way is to create and
index which would create a directory tree like structure in the database
and then turn on the index filesystem mirror options which would create
an actual directory tree and links to the actual stored files but using
the filename of the documents as stored in the database.  This
filesystem mirror of the index can them be shared with Samba_ across the
network.  This access would be read-only, and new versions of the files
would have to be uploaded from the web GUI using the new document
versioning support.

**Mayan EDMS** components are as decoupled from each other as possible,
storage in this case is very decoupled and its behavior is controlled
not by the project but by the Storage progamming class.  Why this design?
All the other part don't make any assumptions about the actual file
storage, so that **Mayan EDMS** can work saving files locally, over the
network or even across the internet and still operate exactly the same.

The file storage behavior is controlled by the :setting:`DOCUMENTS_STORAGE_BACKEND`
and should be set to a class or subclass of Django's ``django.core.files.storage.FileSystemStorage`` class.

.. _Samba: http://www.samba.org/
