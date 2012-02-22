========
Features
========

* :doc:`Document versioning <../topics/versioning>`.

  * Store many versions of the same document, download or revert to a previous version.

* :doc:`Electronic signature verification <../topics/signatures>`.

  * Check the authenticity of documents by verifying their embedded
    cryptographic signatures or upload detached signatures for document
    signed after they were stored.

* Collaboration tools.

  * Discuss documents, comment on new version of a document.

* Office document format support.

  * Word processing files?  Spreadsheets?  Presentations?  They are supported too.

* User defined metadata fields and meta data sets.

  * Metadata fields can be grouped into sets per technical, legal or structural requirements such as the `Dublin core`_
    
* Dynamic default values for metadata.
    
  * Metadata fields can have an initial value which can be static or determined by an user provided Python code snipped.

* Filesystem integration.
    
  * If enabled, the document database index can be mirrored in the filesystem of the hosting computers and shared via Samba_ or any other method to clients computers on a network.
    
* User defined document unique identifier and checksum algorithms.
    
  * Users can alter the default method used to uniquely indentify documents.

* Documents can be uploaded from different sources.

  * Local file or server side file uploads.

* Batch upload many documents with the same metadata.

  * Clone a document's metadata for speedier uploads and eliminate repetitive data entry.

* Previews for a great deal of image formats, including PDF.

  * **Mayan EDMS** provides different file conversion backends with different levels of functionality and requirements to adapt to different deployment environments.

* Full text searching.

  * Document can be searched by their text content, their metadata or any other file attribute such as name, extension, etc.

* Configurable document grouping.
    
  * Automatic linking of documents based on metadata values or document properties.

* :doc:`Roles support <../topics/permissions>`.

  * Users can created an unlimited amount of different roles and are not restricted to the traditional admin, operator, guest paradigm.

* :doc:`Fine grained permissions system <../topics/permissions>`.

  * There is a permission for every atomic operation performed by users.

* Multi page document support.

  * Multiple page PDFs and TIFFs files supported.

* :doc:`Distributed OCR processing <../topics/ocr>`.

  * The task of transcribing text from documents via OCR can be distributed among several physical or virtual computers to decrease load and increase availability.

* Multilingual user interface (English, Spanish, Portuguese, Russian, Polish).

  * **Mayan EDMS** is written using the Django_ framework which natively support Unicode, this coupled with the use of text templates allows **Mayan EDMS** to be translated to practically any language spoken in the world, by default four translations are provided: English, Spanish, Portuguese and Russian.

* :doc:`Multilingual OCR support <../topics/ocr>`.

  * As supported by the OCR engine tesseract.

* Duplicated document search.

* :doc:`Plugable storage backends <../topics/file_storage>` (File based and GridFS included).
    
  * Very easy to use 3rd party plugins such as the ones available for Amazon EC2.

* Color coded tagging.

  * Labeled and color coded tags that are intituitive.

* Staging folders to receive scanned documents directly from network attached scanners.

  * Preview scanned files even before uploading them.


.. _`Dublin core`: http://dublincore.org/metadata-basics/
.. _Samba:  http://www.samba.org/
.. _Django:  https://www.djangoproject.com/
