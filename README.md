Mayan
=============

Open source, Django based document manager with custom metadata indexing, file serving integration and OCR capabilities.

[Website](http://bit.ly/mayan-edms)

Basic requirements
---

Python:

* Django - A high-level Python Web framework that encourages rapid development and clean, pragmatic design.
* django-pagination
* django-filetransfers - File upload/download abstraction
* celery- asynchronous task queue/job queue based on distributed message passing
* django-celery - celery Django integration
* django-mptt - Utilities for implementing a modified pre-order traversal tree in django
* python-magic - A python wrapper for libmagic
* django-taggit - Simple tagging for django
* slate - The simplest way to extract text from PDFs in Python


Execute pip install -r requirements/production.txt to install the python/django dependencies automatically.

Executables:

* tesseract-ocr - An OCR Engine that was developed at HP Labs between 1985 and 1995... and now at Google.
* unpaper - post-processing scanned and photocopied book pages

Optional requirements
---

For the GridFS storage backend:

* PyMongo - the recommended way to work with MongoDB from Python
* GridFS - a storage specification for large objects in MongoDB
* MongoDB - a scalable, open source, document-oriented database

Libraries:

* libmagic - MIME detection library, if not installed Mayan will fall back to using python's simpler mimetype built in library

Mayan has the ability to switch between different image conversion backends, at the moment these two are supported:

* ImageMagick - Convert, Edit, Or Compose Bitmap Images
* GraphicMagick - Robust collection of tools and libraries to read, write, and manipulate an image.

License
-------
This project is open sourced under [GNU GPL Version 3](http://www.gnu.org/licenses/gpl-3.0.html).


Author
------
Roberto Rosario - [Twitter](http://twitter.com/#siloraptor) [E-mail](roberto.rosario.gonzalez at gmail)


Donations
---------
Please [donate](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=W6LMMZHTNUJ6L) if you are willing to support the further development of this project.


Credits
-------
See docs/CREDITS file.


FAQ
---
See docs/FAQ file for common questions and issues.
