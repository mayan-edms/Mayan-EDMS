========
Metadata
========

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

We the ``Lookup`` option is used, it is convenient for the end user to select
from a sorted list. In order to automatically sort the metadata list,
use the python function sorted().

For example, a metadata list of first names may look like this in the Lookup
field of the metadata edit screen::

    ["Markus", "Lyndia", "Bunny", "Glynis", "Juli", "Marie," "Elliot", "Kimberely", "Catherina", "Tobie"]

To insure the user always sees a sorted metadata field when adding metadata
 to a document, write the list like this::

     sorted(["Markus", "Lyndia", "Bunny", "Glynis", "Juli", "Marie," "Elliot", "Kimberely", "Catherina", "Tobie"]).
