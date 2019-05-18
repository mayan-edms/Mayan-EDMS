************
Quick labels
************

Quick labels are predetermined filenames that allow the quick renaming of
documents as they are uploaded or after they have been uploaded.

Quick labels are added and associated to a document type.

Example of quick label: Invoice, Receipt from X store, Purchase order.

It is possible to preserve the file extension when using quick labels.
Extensions are required for some operating system to be able to detect the
correct file type to access the content.

For example if a document file is named "file0001.pdf" and the quick label
"Receipt from X store" is applied, the resulting document label will be
"Receipt from X store.pdf".


Creating quick labels
=====================

.. admonition:: Permissions required
    :class: warning

    The "Edit document types" permission is required for this action, either
    globally or via an ACL for a document type.


Since quick labels are associated with document types, creating quick labels
must be done from the document type view.

#. Go to the :menuselection:`System --> Setup --> Document types` menu.
#. In the document type list, click on the :guilabel:`Quick labels` button of
   the document type for which you wish to create a quick label.
#. In the view titled "Quick labels for document type: <your document type>",
   from the :guilabel:`Actions` dropdown select :guilabel:`Add quick label to document type`.
#. At the quick label creation form enter the desired label and press :guilabel:`Save`.


Using quick labels during upload
================================

#. Use the new document upload wizard from :menuselection:`Documents --> New document`.
#. Select a document type and navigate to the penultimate step, where you have
   the option to drag and drop files to upload.
#. Select a an option from the :guilabel:`Quick document rename` dropdown.
#. Optionally select the :guilabel:`Preserve extension` checkbox to keep the file
   extension.
#. Upload your documents.


Using quick labels for existing documents
=========================================

.. admonition:: Permissions required
    :class: warning

    The "Edit document properties" permission is required for this action, either
    globally or via an ACL for a document or document type.


#. Navigate to the document preview view of the document to rename. Make sure
   quick labels for the document type of the document select have been created.
#. From the :guilabel:`Actions` dropdown select :guilabel:`Edit Properties`.
#. Select a an option from the :guilabel:`Quick document rename` dropdown.
#. Optionally select the :guilabel:`Preserve extension` checkbox to keep the file
   extension.
#. Press :guilabel:`Save` to rename the document.
