==============
Document types
==============

The basic unit of data in Mayan EDMS is the ``document type``. A document
type can be interpreted also as a document category, a document class, or a
document template. Document types need to be created before documents can be
uploaded. It is not possible to upload documents without assigning them a
document type. Examples of document type: **invoices**, **blueprints**,
**receipts**.

.. blockdiag::

   blockdiag {
      default_shape = roundedbox

      document_type [ label = 'Document type' ];
      documents [ label = 'Documents' ];

      document_type -> documents;
   }


Examples:

.. blockdiag::

   blockdiag {
      default_shape = roundedbox

      document_type [ label = 'Invoice' ];
      documents_1 [ label = 'invoice_001.pdf', width=200 ];
      documents_2 [ label = 'invoice_032.pdf', width=200 ];

      document_type -> documents_1, documents_2;
   }


.. blockdiag::

   blockdiag {
      default_shape = roundedbox

      document_type [ label = 'Receipts' ];
      documents_1 [ label = 'groceries_18-01-11.pdf', width=200  ];
      documents_2 [ label = 'car_payment-17-01-02.png', width=200  ];

      document_type -> documents_1, documents_2;
   }


Settings and attributes are applied to document types and documents will
inherit those settings and attributes based on the document type they were
assigned when uploaded into Mayan EDMS. A document can only be of one
type at a given moment, but if needed, the type of a document can be changed.
Upon changing its type, the document will lose its previous settings and
attributes, and will inherit the settings and attributes of its new type.
