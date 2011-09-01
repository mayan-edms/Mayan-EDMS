.. _internals:

=========
Internals
=========

|architecture|

.. |architecture| image:: _static/mayan_architecture.png


**Mayan EDMS** is not a single program, but a collection of different Django apps, each designed to provide a specific functionality.

* ``common`` - Provide a central place to put code, models or templates that are used by all the other apps.
* ``document_indexing``
* ``history``
* ``main`` - Can be thought as the project app, is small on purpose.
* ``navigation`` - Handles the complex automatic creation of hyper text links.
* ``project_setup``
* ``scheduler``
* ``storage`` - Abstracts the storage of documents.
* ``web_theme`` - Handles the presentation of the HTML and CSS to the user.
* ``converter`` - Abstracts the convertions between file formats, calls the backends of which are wrappers for ImageMagick_, GraphicsMagick_ and python's PIL_ coupled with Ghostscript_.
* ``documents`` - The main app, handles the ``Document`` and ``DocumentPage`` classes.
* ``folders``
* ``job_processor``
* ``metadata``
* ``ocr``
* ``project_tools``
* ``smart_settings``
* ``tags`` - Handles document tagging, it is a wrapper for django-taggit_.
* ``document_comments`` - Handles document comments it's a wrapper for `Django\'s comment framework`_.
* ``dynamic_search``
* ``grouping``
* ``mimetype`` - Handles file MIME type detection using python-magic_ or falling back to Python's mimetype library, also handles the MIME type icon library.
* ``permissions`` - All the other apps register their permissions with this one.
* ``sources`` - Handles the document file sources definitions.
* ``user_management`` - User and group management, it is a wrapper for Django's user creating and authentication system.


.. _`Django\'s comment framework`: https://docs.djangoproject.com/en/dev/ref/contrib/comments/
.. _django-taggit:  https://github.com/alex/django-taggit
.. _ImageMagick:  http://www.imagemagick.org/script/index.php
.. _GraphicsMagick: http://www.graphicsmagick.org/
.. _PIL: http://www.pythonware.com/products/pil/
.. _Ghostscript: http://pages.cs.wisc.edu/~ghost/
.. _python-magic:  https://github.com/ahupp/python-magic
