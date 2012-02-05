============
File storage
============

The files are stored and placed under **Mayan EDMS** "control" to avoid
filename clashes (each file gets renamed to its UUID and with an extension)
and stored in a simple flat arrangement in a directory.  This doesn't
stop access to the files but it is not recommended because moving,
renaming or updating the files directly would throw the database out
of sync.  For direct access to the files the recommended way is to create an
:doc:`index <indexes>`, use the indexing mirroring feature and share the result via 
file serving software [#f1]_.

**Mayan EDMS** components are as decoupled from each other as possible,
storage in this case is very decoupled and its behavior is controlled
not by the project but by the Storage progamming class.  Why this design?
All the other part don't make any assumptions about the actual file
storage, so that **Mayan EDMS** can work saving files locally, over the
network or even across the internet and still operate exactly the same.

The file storage behavior is controlled by the :setting:`DOCUMENTS_STORAGE_BACKEND`
and should be set to a class or subclass of Django's ``django.core.files.storage.FileSystemStorage`` class.

.. rubric:: Footnotes

.. [#f1] http://en.wikipedia.org/wiki/File_server
