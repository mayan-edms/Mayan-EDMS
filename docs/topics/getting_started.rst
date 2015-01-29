===============
Getting started
===============

Before starting to use **Mayan EDMS**, two things need to be configured:

- At least one document source
- At least one document type

Document sources
----------------

Document sources define from where documents will be uploaded or gathered.
To do add a document source go to the ``Setup`` section, then to the ``Sources`` section.
To obtain the fastest working setup, create a new source of type ``Web forms``.
``Web forms`` are just HTML forms with a ``Browse`` button that will open the file upload
dialog when clicked. Name it something simple like ``Local documents`` and select whether or not
compressed files uploaded from this source will be automatically decompressed and
their content treated as individual documents.

Document types
--------------

Examples of document types are: ``Legal documents``, ``Internal documents``, ``Medical records``, ``Designing specifications``, ``Permits``.
A document type represent a class of documents which share some common property.
A good indicator that can help you determine your document types is what kind of
information or ``metadata`` is attached to those documents.

Once a document source and a document type have been created you have all the minimal
elements required to start uploading documents.

Defining metadata
-----------------

With your document types defined it should be much easier now to define the required
``metadata`` for each of these document types. When creating ``metadata`` types,
the first thing that will be needed is the internal name with which this metadata
type will be referenced in other areas of **Mayan EDMS**. Internal name is like a
variable so it should not contain spaces or uppercase characters. After the internal name,
enter the name that will be visible to you and your users, this is usually the same as the
internal name but with proper capitalization and spacing. The ``metadata types``
can have default values to speed up data entry. They can be single number or a
words enclosed in quotes, ie::

    "Building A"

or::

    "Storage room 1"

Default values can also be defined as ``Python`` statements or functions such as::

    current_date()

If you want to restrict or standardize the values for a metadata type, use the ``Lookup`` field to
define the list of options that are allowed. Define the lookup list using a ``Python``
list of quoted values, for example::

    ["2000", "2001", "2002", "2003", "2004"].

Instead of a free entry text field, your users will get a dropdown list of years,
this will ensure an unified data entry formatting. You can also use a
``Python`` expression to generate the lookup list.

Metadata types can be assigned in two ways to a document type, by making it an
optional or a required metadata type for a specific document. This method
allows metadata that is very important to some types of documents, like Invoice
numbers to Invoices to be required in other for an Invoice to be able to be uploaded.
Accordingly optional metadata types will presented but users are not required to
enter a value in other to be able to upload a document.

Indexes
-------

After defining all your metadata types you can also define indexes to
let **Mayan EDMS** to automatically categorize your documents based on their metadata values.
To create an index to organize invoices by a year metadata field do the following:

- Create a year metadata type with the name ``year`` and the label ``Year``.
- Create an invoice document type and assign it the ``year`` metadata type as a required metadata type.
- Create a new index, give it the name ``invoices_per_year`` and the label ``Invoices per year``.
- Edit the index's ``Tree template``, add a ``New child node``, and enter ``document.metadata_value_of.year`` as the ``Indexing expression``, check the ``Link documents`` checkbox and save.
- Link this new index to the invoice document type using the ``Document types`` button of the index.

Now every time a new invoice upload or an existing invoice's ``year`` metadata value is changed, a new folder will be created in the ``Invoices`` index with the corresponding invoices for that year.
