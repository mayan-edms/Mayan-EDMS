========
Features
========

* :doc:`Document versioning <../topics/versioning>`.

  * Store many versions of the same document, download or revert to a previous
    version.

* :doc:`Electronic signature verification <../topics/signatures>`.

  * Check the authenticity of documents by verifying their embedded
    cryptographic signatures or upload detached signatures for document
    signed after they were stored.

* Collaboration tools.

  * Discuss documents, or comment on new versions of a document.

* Office document format support.

  * Mayan EDMS can detect the presence of Libre Office and use it to support
    word processing files, spreadsheets and presentations.

* User defined metadata fields.

  * Several metadata fields can be matched to a document type as per technical,
    legal or structural requirements such as the `Dublin core`_.

* Dynamic default values for metadata.

  * Metadata fields can have an initial value, which can be static or determined
    by a template code snippet provided by the user.

* Documents can be uploaded from different sources.

  * Local file or server side file uploads, multifunctional copier, or even via
    email.

* Batch upload many documents with the same metadata.

  * Clone a document's metadata for speedier uploads and eliminate repetitive
    data entry.

* Previews for many file formats.

  * Mayan EDMS provides image preview generation for many popular file
    formats.

* Full text searching.

  * Documents can be searched by their text content, their metadata or any other
    file attribute such as name, extension, etc.

* Configurable document grouping.

  * Automatic linking of documents based on metadata values or document
    properties.

* :doc:`Roles support <../topics/permissions>`.

  * It is possible to create an unlimited amount of different roles not being
    restricted to the traditional admin, operator, guest paradigm.

* :doc:`Fine grained permissions system <../topics/permissions>`.

  * There is a permission for every atomic operation performed by users.

* Multi page document support.

  * Multiple page PDF and TIFF files are supported.

* Automatic OCR processing.

  * The task of transcribing text from documents via OCR can be distributed
    among several physical or virtual computers to decrease load and increase
    availability.

* Multilingual user interface.

  * Mayan EDMS being written using the Django_ framework, can be translated
    to practically any language spoken in the world. For a list of translated
    languages have a look at the Transifex_ project location.

* Multilingual OCR support.

  * The current language of the document is passed to the corresponding OCR
    engine to increase the text recognition rate.

* :doc:`Plugable storage backends <../topics/file_storage>`.

  * It is very easy to use 3rd party plugins such as the ones available for
    Amazon EC2.

* Color coded tagging.

  * Labeled and color coded tags can be assigned for intuitive recognition.

* Workflows.

  * Keep track of the state of documents, along with the log of the previous
    state changes.


.. _`Dublin core`: http://dublincore.org/metadata-basics/
.. _Django:  https://www.djangoproject.com/
.. _Transifex: https://www.transifex.com/projects/p/mayan-edms/
