============
Requirements
============
**Mayan EDMS** supports various levels of functionality, because of this
requirements can vary for each individual deployment.

Basic requirements
==================

Python:

* ``Django`` - A high-level Python Web framework that encourages rapid development and clean, pragmatic design.
* ``django-pagination``
* ``django-filetransfers`` - File upload/download abstraction
* ``django-mptt`` - Utilities for implementing a modified pre-order traversal tree in django
* ``django-taggit`` - Simple tagging for django
* ``slate`` - The simplest way to extract text from PDFs in Python


Execute pip install -r requirements/production.txt to install the python/django dependencies automatically.

Executables:

* ``tesseract-ocr`` - An OCR Engine that was developed at HP Labs between 1985 and 1995... and now at Google.
* ``unpaper`` - post-processing scanned and photocopied book pages

Optional requirements
=====================

To enable distributed OCR support
---------------------------------

* ``celery`` - asynchronous task queue/job queue based on distributed message passing
* ``django-celery`` - ``celery`` Django integration

To store documents in a GridFS database
---------------------------------------

* ``PyMongo`` - the recommended way to work with ``MongoDB`` from Python
* ``GridFS`` - a storage specification for large objects in ``MongoDB``
* ``MongoDB`` - a scalable, open source, document-oriented database

Enhanced MIME detection
------------------------

* ``libmagic`` - MIME detection library, if not installed **Mayan EDMS** will fall back to using python's simpler mimetype built in library
* ``python-magic`` - A python wrapper for libmagic

Image conversion backends
-------------------------
**Mayan EDMS** has the ability to switch between different image conversion backends, at the moment these three are supported:

* ``ImageMagick`` - Convert, Edit, Or Compose Bitmap Images.
* ``GraphicMagick`` - Robust collection of tools and libraries to read, write, and manipulate an image.
* Python only - Relies on ``PIL`` to support a limited set of the most common graphics formats.

By default the python backend is used.
