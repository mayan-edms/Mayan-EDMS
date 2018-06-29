====================
Access control lists
====================

Besides the permissions system explained in :doc:`permissions`, Mayan EDMS
provides per object permission granting. This feature is used to grant a
permission to a role, but this permission can only be executed for a limited
number of objects (documents, folders, tags) instead of being effective
system-wide.

.. blockdiag::

   blockdiag {
      default_shape = roundedbox

      document [ label = 'Document' ];
      role [ label = 'Role' ];
      permission [ label = 'Permission' ];

       role -> permission -> document;
   }

Example:

.. blockdiag::

   blockdiag {
      default_shape = roundedbox

      document [ label = '2015 Payroll report.txt', width=200 ];
      role [ label = 'Accountants' ];
      permission [ label = 'View document' ];

      role -> permission -> document;
   }

In this scenario only users in groups belonging to the ``Accountants`` role
would be able to view the ``2015 Payroll report.txt`` document.

Inherited access control
========================

It is also possible to grant a permission to a role for a specific document type (:doc:`document_types`).
Under this scheme all users in groups belonging to that role will inherit that
permission for all documents of that type.

.. blockdiag::

   blockdiag {
      default_shape = roundedbox
      document_type [ label = 'Document type' ];
      role [ label = 'Role' ];
      permission [ label = 'Permission' ];
      documents [shape = "note", stacked];

       role ->  permission -> document_type ;
       document_type -> documents [folded, label = "inherit" ];
   }

Example:

.. blockdiag::

   blockdiag {
      default_shape = roundedbox
      document_type [ label = 'Payroll reports', width=200 ];
      role [ label = 'Accountants' ];
      permission [ label = 'View document' ];
      documents [shape = "note", stacked, label="payroll_report*.pdf" ];

      role -> permission -> document_type ;
       document_type -> documents [folded, label = "inherit" ];
   }

The role ``Accountants`` is given the permission ``document view`` for the
document type ``Payroll reports``. Now all users in groups belonging to the
``Accountants`` role can view all documents of the type ``Payroll reports``
without needing to have that permissions granted for each particular
``Payroll reports`` type document.

If access control for the ``Payroll reports`` documents needs to be updated it
only needs to be done for the document type and not for each document of the type
``Payroll reports``.
