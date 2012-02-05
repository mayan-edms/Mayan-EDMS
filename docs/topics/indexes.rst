=======
Indexes
=======

Administrators first define the template of the index and an instance
of the index is then auto-populated with links to the documents depending
on the rules of each branch of the index evaluated againts the metadata
of the documents.  Indexes can be mirrored to the operating system filesystem
using the configuration option
:setting:`DOCUMENT_INDEXING_FILESYSTEM_SERVING`.  This creates an actual
directory tree and links to the actual stored files but using
the filename of the documents as stored in the database.  This
filesystem mirror of the index can them be served with Samba_ across the
network.  This access would be read-only, and new versions of the files
would have to be uploaded from the web GUI using the new document
versioning support.

The index cannot be edited manually, only changing
the rules or the metadata of the documents would cause the index to be
regenerated.  For manual organization of documents there are the folders,
their structure is however flat, and they have to be manually updated and
curated.

.. _Samba: http://www.samba.org/
