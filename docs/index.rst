Welcome to Mayan EDMS!
======================

**Mayan EDMS** is a `Free Open Source`_ `Electronic Document Management System`_, coded in
the Python language using the Django_ web application framework and released
under the `Apache 2.0 License`_. It provides an electronic vault or repository for electronic documents.

The easiest way to install and try **Mayan EDMS** is by using a Debian based Linux distribution
and installing it from PyPI with the following commands:

.. code-block:: bash

    sudo apt-get install libjpeg-dev libmagic1 libpng-dev libreoffice libtiff-dev gcc ghostscript gpgv python-dev python-virtualenv tesseract-ocr unpaper poppler-utils -y
    virtualenv venv
    source venv/bin/activate
    pip install mayan-edms
    mayan-edms.py initialsetup
    mayan-edms.py runserver

Point your browser to 127.0.0.1:8000 and use the automatically created admin
account.

.. image:: /_static/overview.gif
   :alt: Overview

.. toctree::
    :hidden:

    Features <topics/features>
    Installation <topics/installation>
    Deploying <topics/deploying>
    Release notes and upgrading <releases/index>
    Concepts <topics/index>
    Development <topics/development>
    App creation <topics/app_creation>
    Translations <topics/translations>
    Contributors <topics/contributors>
    Screenshots <topics/screenshots>
    Licensing <topics/license>
    FAQ <topics/faq>
    Contact <topics/contact>

.. _Django: http://www.djangoproject.com/
.. _Free Open Source: http://en.wikipedia.org/wiki/Open_source
.. _Electronic Document Management System: https://en.wikipedia.org/wiki/Document_management_system
.. _Apache 2.0 License: https://www.apache.org/licenses/LICENSE-2.0.txt
