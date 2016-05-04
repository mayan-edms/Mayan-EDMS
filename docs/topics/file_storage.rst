============
File storage
============

The files are stored and placed under Mayan EDMS "control" to avoid
filename clashes each file gets renamed to its ``UUID`` (Universally Unique ID),
without extension, and stored in a simple flat arrangement in a directory.

.. blockdiag::

   blockdiag {
      file [ label = 'mayan_1-1.pdf', width=120];
      document [ label = 'mayan/media/document_storage/ab6c1cfe-8a8f-4a30-96c9-f54f606b9248', width=450];
      file -> document [label = "upload"];

      file -> document;
   }

This doesn't stop access to the files but renaming, moving or updating
directly them is not recommended because it would throw the database out
of sync.

Because Mayan EDMS components are as decoupled from each other as possible,
storage in this case is decoupled and its behavior is controlled
not by the project but by the ``Storage`` module class. All the other
modules don't make any assumptions about how the actual document files are
stored. This way files can be saved locally, over the network or even across
the Internet and everything will still operate exactly the same.

The default file storage backend: ``storage.backends.filebasedstorage.FileBasedStorage``
is a simple backend that only supports paths and not IP addresses. In case you
are interested in using remote volumes to store documents (NFS, SAMBA), first
mount these volumes so that they appear as a directories to Mayan EDMS. For
direct support for remote volumes a custom backend would be needed such as those
provided by the Django Storages project (https://django-storages.readthedocs.org/en/latest/).
