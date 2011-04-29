Mayan
=============

Open source, Django based document manager with custom metadata indexing, file serving integration and OCR capabilities.
(http://bit.ly/mayan-edms)

Requirements
---

Python:

* Django - A high-level Python Web framework that encourages rapid development and clean, pragmatic design.
* django-pagination
* django-filetransfers - File upload/download abstraction
* celery- asynchronous task queue/job queue based on distributed message passing
* django-celery - celery Django integration

For the GridFS storage backend:

* PyMongo - the recommended way to work with MongoDB from Python
* GridFS - a storage specification for large objects in MongoDB
* MongoDB - a scalable, open source, document-oriented database

Or execute pip install -r requirements/production.txt to install the dependencies automatically.

Executables:

* libmagic - MIME detection library
* tesseract-ocr - An OCR Engine that was developed at HP Labs between 1985 and 1995... and now at Google.
* unpaper - post-processing scanned and photocopied book pages
* ImageMagick - Convert, Edit, Or Compose Bitmap Images
* GraphicMagick - Robust collection of tools and libraries to read, write, and manipulate an image.

License
-------
GPL Version 3


Author
------

Roberto Rosario - [Twitter](http://twitter.com/#siloraptor) [E-mail](roberto.rosario.gonzalez at gmail)


Credits
-------
See docs/CREDITS file.


FAQ
---
See docs/FAQ file for common questions and issues.
