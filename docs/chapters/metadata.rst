********
Metadata
********

Metadata is the name of the attribute of a document. The concept of metadata is
divided in two: **metadata types** (size, color, distance) and **metadata values** for
those types. Metadata types are defined in the setup menu and associated with
document types. Then when a document is uploaded, a value for that metadata
can be entered. There are two kinds of metadata type to document type relations:
optional and required. When a metadata type is optional for a document type,
it can be left blank for a document being uploaded and the upload will still
be successful. On the other hand required metadata type must be given a value
or it will not be possible to upload the document at hand.

Examples of metadata type: Invoice number, color, employee id.

The data entry of metadata types can be set to allow any value to be provided
(the default) or a list of possible values can be entered in the ``Lookup``
configuration option and users will be presented with a drop down list of options
instead of the default text entry box.

If metadata types are setup to allow any value to be entered a ``validation``
option can be chosen to block the entry of invalid data. Metadata types also
provide ``parsers`` which will not block the entry of data but are able to
interpret and modify the value provided by the user to a conform to a specific
format. An example of a provided parser is the date parser which will interpret
and correct dates provided by users regardless of the format in which they are
entered.


Creating metadata types
=======================

.. admonition:: Permissions required
    :class: warning

    The "Create new metadata types" permission is required for this action.


#. Go to the :menuselection:`System --> Setup --> Metadata types` menu.
#. From the :guilabel:`Actions` dropdown select :guilabel:`Create new`.
#. Provide a name to reference this metadata type in other parts of the system.
#. Enter a label to be shown to users when using this metadata type.
#. Optional: Enter a default value for the metadata type.
#. Optional: Provide a comma separated list of options to restrict the data entry
   when using this metadata type.
#. Optional: Select a validator and a parser to validate and cleanup the data
   entry when not using a predetermined list of values.
#. Press :guilabel:`Submit`.


Assigning a metadata type to a document type
============================================

.. admonition:: Permissions required
    :class: warning

    - The "Edit metadata types" permission is required for this action, globally or
      via an ACL for a metadata type.
    - Also the "Edit document type" permission
      is required, globally or via an ACL for a document type.


This action can be performed in two ways.

Option 1: Via the metadata type view
------------------------------------

#. Go to the :menuselection:`System --> Setup --> Metadata types` menu.
#. Click on the button :guilabel:`Document types` of the metadata type you which
   to associate.
#. From the list of existing document types press either:

   - :guilabel:`None` if this metadata type will not be available for documents
     of the type.
   - :guilabel:`Optional` if this metadata type will be available and is
     optional to provide a value for documents of the type.
   - :guilabel:`Required` if this metadata type will be available and is
     required to provide a value for documents of the type.

#. Press :guilabel:`Save`.


Option 2: Via the document type view
------------------------------------

#. Go to the :menuselection:`System --> Setup --> Document types` menu.
#. Click on the button :guilabel:`Metadata types` of the metadata type you which
   to associate.
#. From the list of existing metadata types press either:

   - :guilabel:`None` if this metadata type will not be available for documents
     of the type.
   - :guilabel:`Optional` if this metadata type will be available and is
     optional to provide a value for documents of the type.
   - :guilabel:`Required` if this metadata type will be available and is
     required to provide a value for documents of the type.

#. Press :guilabel:`Save`.
