============
Requirements
============
**Mayan EDMS** supports various levels of functionality, because of this
requirements can vary for each individual deployment.

Basic requirements
==================

Python:

* ``Django`` - A high-level Python Web framework that encourages rapid development and clean, pragmatic design.

Execute pip install -r requirements/production.txt to install the python/django dependencies automatically.

Executables:

* ``gpg`` - The GNU Privacy Guard

Optional requirements
=====================

Improved OCR
------------

* ``unpaper`` - post-processing scanned and photocopied book pages

Enhanced MIME detection
------------------------

* ``libmagic`` - MIME detection library, if not installed **Mayan EDMS** will fall back to using python's simpler mimetype built in library
* ``python-magic`` - A python wrapper for libmagic


OCR backends
------------
** Mayan EDMS** can make use of different OCR engines via OCR backends. By default it will use the ``Tesseract OCR backend``.

* ``tesseract-ocr`` - An OCR Engine that was developed at HP Labs between 1985 and 1995... and now at Google.  Version 3.x or greater required.


Image conversion backends
-------------------------
**Mayan EDMS** has the ability to switch between different image conversion backends, at the moment these three are supported:

* ``ImageMagick`` - Convert, Edit, Or Compose Bitmap Images.
* ``GraphicMagick`` - Robust collection of tools and libraries to read, write, and manipulate an image.
* Python only - Relies on ``Pillow`` to support a limited set of the most common graphics formats.

By default the python backend is used.
