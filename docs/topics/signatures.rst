===================
Document signatures
===================

**Mayan EDMS** supports two types of document signatures: embedded and
detached signatures. When a document with an embedded signature is
uploaded, this signature is readily detected as part of the document
inspection step. The status of the signature can be verified by accessing the
signatures sections of a document.

Existing non signed documents can be signed in one of two ways:
by downloading the document, signing it, and uploading the signed document
as a new version of the existing one or by creating a detached signature for
the non signed document and uploading such detached signature file.

Maintenance of the public keyring can be done using the ``Key management``
functionality in the ``Setup menu``.

From this menu, key servers can be queried and the results imported. Public
keys no longer needed can also be deleted from this menu.

Only `GNU Privacy Guard`_ signatures are support at the moment.

.. _`GNU Privacy Guard`: www.gnupg.org/
