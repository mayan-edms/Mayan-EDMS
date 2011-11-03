========
Features
========

* User defined metadata fields and meta data sets.

    * Metadata fields can be grouped into sets per technical, legal or structural requirements such as the `Dublin core`_
    
.. _`Dublin core`: http://dublincore.org/metadata-basics/
    
* Dynamic default values for metadata.
    
    * Metadata fields can have an initial value which can be static or determined by an user provided Python code snipped.

* Filesystem integration.
    
    * If enabled, the document database index can be mirrored in the filesystem of the hosting computers and shared via Samba_ or any other method to clients computers on a network.
    
.. _Samba:  http://www.samba.org/

* User defined document unique identifier and checksum algorithms.
    
    * Users can alter the default method used to uniquely indentify documents.

* Documents can be uploaded from different sources.

    * Local file or server side file uploads.

* Batch upload many documents with the same metadata.
* Previews for a great deal of image formats, including PDF.

    * **Mayan EDMS** provides different file conversion backends with different levels of functionality and requirements to adapt to different deployment environments.

* Full text searching.
* Configurable document grouping.
    
    * Automatic linking of documents based on metadata values or document properties.

* Permissions and roles support.

    * User can created many different roles and are not limited to the traditional limited admin, operator, guest paradigm.

* Multi page document support.

    * Multiple page PDFs and TIFFs files supported.

* Distributed OCR processing.

    * The task of transcribing text from documents via OCR can be distributed among several physical or virtual computers to decrease load and increase availability.

* Multilingual user interface (English, Spanish, Portuguese, Russian).

    * **Mayan EDMS** is written using the Django_ framework which natively support Unicode, this coupled with the use of text templates allows **Mayan EDMS** to be translated to practically any language spoken in the world, by default four translations are provided: English, Spanish, Portuguese and Russian.
    
.. _Django:  https://www.djangoproject.com/

* Multilingual OCR support.
* Duplicated document search.
* Plugable storage backends (File based and GridFS included).
* Color coded tagging.
* Staging folders to receive scanned documents directly from network attached scanners.
