Mayan
=============

Open source, Django based document manager with custom metadata indexing, file serving integration and OCR capabilities.
 
![screenshot](http://img339.imageshack.us/img339/3116/newfullscreenshot2.png)


Features
---

* User defined metadata fields
* Dynamic default values for metadata
* Lookup support for metadata
* Filesystem integration by means of metadata indexing directories
* User defined document uuid generation
* Local file or server side staging file uploads
* Batch upload many documents with the same metadata
* User defined document checksum algorithm
* Previews for a great deal of image formats, including PDF
* Search documents by any field value
* Group documents by metadata automatically
* Permissions and roles support
* Multi page document support
* Page transformations
* Distributed OCR processing
* Multilingual (English, Spanish)
* Duplicated document search
* Upload multiple documents inside a ZIP file 
* Plugable storage backends (File based and GridFS included)

Requirements
---

Python:

* Django - A high-level Python Web framework that encourages rapid development and clean, pragmatic design.
* django-pagination
* django-filetransfers - File upload/download abstraction
* celery - asynchronous task queue/job queue based on distributed message passing
* django-celery - celery Django integration

For the GridFS storage backend:

* PyMongo - the recommended way to work with MongoDB from Python
* GridFS - a storage specification for large objects in MongoDB

Or execute pip install -r requirements/production.txt to install the dependencies automatically.

Executables:

* ImageMagick - Convert, Edit, Or Compose Bitmap Images
* libmagic - MIME detection library
* tesseract-ocr - An OCR Engine that was developed at HP Labs between 1985 and 1995... and now at Google.
* unpaper - post-processing scanned and photocopied book pages
* MongoDB - a scalable, open source, document-oriented database

License
-------
See docs/LICENSE file.


Author
------

Roberto Rosario - [Twitter](http://twitter.com/#siloraptor) [E-mail](roberto.rosario.gonzalez at gmail)


Credits
-------
See docs/CREDITS file.


FAQ
---
See docs/FAQ file for common questions and issues.
