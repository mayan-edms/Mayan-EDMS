=======
Indexes
=======
To configure: |Setup tab| |Right arrow| |Indexes button| |Right arrow| |Tree template link|

To use: |Index tab|

Indexes are an automatic method to hierarchically organize documents in relation to their metadata and to each other.

Index templates
===============

Since multiple indexes can be defined, the first step is to create an empty index.
Administrators then define the tree template showing how the index will be structured.
Each branch can be a pseudo folder, which can hold other child 'folders' or
a document container which will have all the links to the documents that
matched the path to reach the document container.

.. image:: index_template.png
 :alt: index template

Index instances
===============

The template is the skeleton from which an instance of the index is then
auto-populated with links to the documents depending on the rules of each
branch of the index evaluated against the metadata and properties of the documents.

.. image:: index_instance.png
 :alt: index instance

Index serving
=============

Indexes can be mirrored to the operating system filesystem
using the configuration option
:setting:`DOCUMENT_INDEXING_FILESYSTEM_SERVING`.
 
``settings_local.py``::

  # Supposing the 'Sample index' internal name is 'sample_index'
  DOCUMENT_INDEXING_FILESYSTEM_SERVING = {
    'sample_index': '/var/local/document/sharing/invoices/',
  }

This creates an actual directory tree and links to the actual stored files but using
the filename of the documents as stored in the database. 

.. image:: indexes.png
 :alt: indexes diagram

This filesystem mirror of the index can them be served with Samba_ across the
network.  This access would be read-only, with new versions of the files
being uploaded from the web GUI using the document versioning support.

The index cannot be edited manually to protect it's integrity, only changing
the rules or the metadata of the documents would cause the index to be
regenerated.  For manual organization of documents there are the folders,
their structure is however flat, and they have to be manually updated and
curated. 

.. _Samba: http://www.samba.org/

.. |Setup tab| image:: /_static/setup_tab.png
 :alt: Setup tab
 :align: middle

.. |Right arrow| image:: /_static/arrow_right.png
 :alt: Right arrow
 :align: middle

.. |Indexes button| image:: /_static/indexes_button.png
 :alt: Indexes button
 :align: middle

.. |Tree template link| image:: /_static/tree_template_link.png
 :alt: Tree template link
 :align: middle

.. |Index tab| image:: /_static/index_tab.png
 :alt: Index tab
 :align: middle
