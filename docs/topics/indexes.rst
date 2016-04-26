=======
Indexes
=======

Indexes are an automatic method to hierarchically organize documents in
relation to their properties (:doc:`metadata`, label, MIME type, etc). To use
indexes you need to first create an index template. Once created, associate
the index to one or more :doc:`document_types`.

Index are hierarchical models so a tree template needs to be specified for them.
This tree template will contain references to document metadata or properties
that will be replaced with the actual value for those metadata or properties.

Example:

- Document type: ``Product sheet``
- Metadata type: ``Product year``, associated as a required metadata for the document type ``Product sheet``.

- Index: ``Product sheets per year``, and associated to the document type ``Product sheet``.
- Index slug: ``product-sheets-per-year``. Slugs are internal unique identifiers that can be used by other Mayan EDMS modules to reference each index.
- Index tree template as follows:

.. blockdiag::

   blockdiag {
      index [ label = 'Product sheets per year', width=180 ];
      root [ label = 'Root (Has document links? No)', width=450];
      level_2 [ label = '{{ document.metadata_value_of.product_year }} (Has document links? Yes)', width=450];

      group {
        label = "Tree template";
        color = "#dddddd";
        style = dashed;
        root; level_2;
      }

      index -> root
      root -> level_2 [folded];
   }

Now every time a new ``Product sheet`` is uploaded a hierarchical unit with the value
of the metadata type ``Product year`` is created and a link to the uploaded ``Product sheet`` added to it.

Example:

Suppose three ``Product sheets`` are uploaded with the following values as their
``Product year`` metadata: 2001, 2002, 2001 respectively. The result index
that will be generate based on the tree template would be as follows:

.. blockdiag::

   blockdiag {
      index [ label = 'Product sheets per year', width=180 ];
      year_1 [ label = '2001', width = 60 ];
      year_2 [ label = '2002', width = 60 ];
      document_1 [ label = 'Product A data sheet (2001)', width = 200 ];
      document_2 [ label = 'Product B data sheet (2002)', width = 200 ];
      document_3 [ label = 'Product C data sheet (2001)', width = 200 ];

      group {
        label = "Index content";
        color = "#dddddd";
        style = dashed;
        year_1, year_2, document_1, document_2, document_3;
      }

      index -> year_1;
      index -> year_2;
      year_1 -> document_1;
      year_2 -> document_2;
      year_1 -> document_3;

   }

Mirroring
=========

Indexes can be exported as `FUSE <https://en.wikipedia.org/wiki/Filesystem_in_Userspace>`_
filesystems. Using the management command ``mountindex`` we could export the
previous example index as follows::

    mkdir -p ~/indexes/products
    mayan-edms.py mountindex product-sheets-per-year ~/indexes/products

The ``~/indexes/products`` directory will now have a directory and files structure
identical to that of the index. Once indexes are mounted with this command, they
behave like any other filesystem directory and can even be further shared
via the network with network file system software like
`Samba <https://www.samba.org/>`_ or
`NFS <https://en.wikipedia.org/wiki/Network_File_System>`_.

Indexes and mirrored indexes are Read Only as they are generated as a result of
prior activities like document uploads, metadata changes.
