===============
Getting started
===============

This chapter will guide you through the initial steps needed to get **Mayan EDMS**
up and running after installation.

The easy 2 step setup
=====================

Document sources
----------------
|Setup tab| |Right arrow| |Sources button| |Right arrow| |Web form tab|
 
Before anything else you must define from where you will feed **Mayan EDMS**
document for it to process and store.  To do this first go to the ``Setup`` tab
then to the ``Sources`` button.  To obtain the fastest working setup, create a
new source of type ``Web forms``.  This source will open a browser file upload
dialog, hence the name ``Web forms``.  Name it something simple like ``Local documents``,
choose an icon to visually identify this document if you so wish and select whether or not
compressed files uploaded from this source will be automatically decompressed and
their content treated as individual documents.


Quickly bootstraping your Mayan EDMS install
--------------------------------------------
|Setup tab| |Right arrow| |Bootstrap button|

**Mayan EDMS** now includes an app called ``Bootstrap``.  This app stores
scripted configurations, that when executed will setup your installation of **Mayan EDMS**.
From there you can then fine tune this setup to your needs.  To use this
app go to the ``Setup`` area and launch the app using the ``Bootstrap`` button.

The longer custom setup
=======================

Setting your document types
---------------------------
|Setup tab| |Right arrow| |Document types button|

If none of the available bootstrap setups fit your needs and your wish to
setup **Mayan EDMS** from scratch the first thing to consider are which are
going to be your document types.  Examples of document types are: ``Legal documents``,
``Internal documents``, ``Medical records``, ``Desging specifications``, ``Permits``.
A document type represent a group, a type, a class of documents which share some
common properties.  A good indicator that can help you determine you document types
is what kind of information or ``metadata`` is attached to the documents.


Defining metadata
-----------------
|Setup tab| |Right arrow| |Metadata types button|

With your document types defined it should be much easier now to define the required
``metadata`` for each of these document types.  When creating ``metadata`` types,
the first thing that will be needed is the internal name with which this metadata
type will be references in other areas of **Mayan EDMS**.  Internal name is like a
variable so it should not contain spaces or uppercase characters.  After the internal name,
enter the name that will visible to you and your users, this is usuall the same as the
internal name but with proper capitalization and spacing.  ``metadata`` types
can have default values to speed up data entry, default static values are enclosed in
quotes, ie::

    "Building A"
    
or::

    "Storage room 1"
    
Default values can also be defined as ``Python`` statements or functions such as::

    current_date()
    
If you want to restrict or standardize the values for a metadata type, use the ``Lookup`` field to
define the list of options that are allowed.  Define the lookup list using a ``Python``
list of quoted values, for example::

    ["2000", "2001", "2002", "2003", "2004"].

Instead of a free entry text field, your users will get a dropdown list of years.
You can also use a ``Python`` expression to generate the lookup list.

When you are uploading new document a choice of metadata types will be presented
and you choose which of those you wish to enter for the document you are about
to upload.  To speed data entry you can also match which metadata types will
be preselected when uploading a document of certain type.  To match metadata types
to document types, go to the ``setup`` tab, ``document types`` button, and
lastly ``Default metadata``.  Choose the desired metadata for the document type
currently selected and press ``Add``.  From now on whenever you upload a document of
this type, the related metadata types for this document type will be preselected.

After defining all your metadata types you can also define your indexes to
let **Mayan EDMS** automatically categorize your documents based on their metadata.
Refer to the chapter named :doc:`Indexes </topics/indexes>` for examples on how to use the document indexes. 


.. |Setup tab| image:: /_static/setup_tab.png
 :alt: Setup tab
 :align: middle

.. |Sources button| image:: /_static/sources_button.png
 :alt: Sources button
 :align: middle

.. |Web form tab| image:: /_static/web_form_source_tab.png
 :alt: Web form tab
 :align: middle

.. |Bootstrap button| image:: /_static/bootstrap_button.png
 :alt: Bootstrap button
 :align: middle
 
.. |Right arrow| image:: /_static/arrow_right.png
 :alt: Right arrow
 :align: middle

.. |Document types button| image:: /_static/document_types_button.png
 :alt: Document types button
 :align: middle

.. |Metadata types button| image:: /_static/metadata_types_button.png
 :alt: Metadata types button
 :align: middle
