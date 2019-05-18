*******************
Document versioning
*******************

Mayan EDMS has the ability to store different versions of the same
document. A comment field is provided to allow users to summarize the new
version changes in comparison with the previous one. If a new version was
uploaded by mistake or such new version is no longer necessary the option to
revert to a previous version of the document is provided.

.. blockdiag::

   blockdiag {
      default_shape = roundedbox
      orientation = portrait
        node_width = 200;
      version_1 [ label = "Version 1" ];
      version_2 [ label = "Version 2" ];
      document_1 [ label = "payroll_report.pdf" ];
      document_2 [ label = "payroll_report_fixed.pdf" ];
      upload_1 [ label = "payroll_report.pdf" ];
      upload_2 [ label = "payroll_report_fixed.pdf" ];

        upload_1 -> version_1 -> document_1;
        upload_2 -> version_2 -> document_2;
        document_1 -> document_2;
   }

Only the interactive document sources (:doc:`../chapters/sources`)
(``Web`` and ``Staging folders``) are available to upload new document versions.

There is no limit to the number of versions a document can have.

.. blockdiag::

    blockdiag {
        default_shape = roundedbox
        orientation = portrait
        node_width = 200;

        document [ label = "payroll_report.pdf" ];
        versions [ label = "Versions", stacked ];

        document -> versions;
   }

By default, the last version will be showed when working with the document
but any of the versions can be inspected and viewed.


View a document version list
============================

.. admonition:: Permissions required
    :class: warning

    The "View documents' versions list" permission is required for this action,
    either globally or via an ACL for a document or document type.


#. Navigate to the select document's preview view.
#. Click on the sibebar's :guilabel:`Versions` button.


Uploading a new document version
================================

.. admonition:: Permissions required
    :class: warning

    The "Create new document versions" permission is required for this action,
    either globally or via an ACL for a document or document type.


#. Navigate to the select document's versions list view.
#. From the :guilabel:`Actions` dropdown select :guilabel:`Upload new version`.
#. Optionally type a comment explaining the changes in the new version.
#. Press the :guilabel:`Browse` button and select a new file.
#. Press :guilabel:`Save` upload the new verision.

