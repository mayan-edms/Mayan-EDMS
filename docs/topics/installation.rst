============
Installation
============

Mayan EDMS should be deployed like any other Django_ project and
preferably using virtualenv_.

Being a Django_ and a Python_ project, familiarity with these technologies is
recommended to better understand why Mayan EDMS does some of the things it
does.

Bellow are the step needed for a test install.

Binary dependencies
===================

Ubuntu
------

If using a Debian_ or Ubuntu_ based Linux distribution, get the executable
requirements using::

    sudo apt-get install libjpeg-dev libmagic1 libpng-dev libreoffice libtiff-dev gcc ghostscript gpgv python-dev python-virtualenv tesseract-ocr poppler-utils -y


Mac OSX
-------

Mayan EDMS is dependent on a number of binary packages and the recommended
way is to use a package manager such as `MacPorts <https://www.macports.org/>`_
or `Homebrew <http://brew.sh/>`_.


Use MacPorts to install binary dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With MacPorts installed run the command:

.. code-block:: bash

    sudo port install python-dev gcc tesseract-ocr unpaper \
    python-virtualenv ghostscript libjpeg-dev libpng-dev \
    poppler-utils

Set the Binary paths
********************

Mayan EDMS by default will look in /usr/bin/ for the binary files it needs
so either you can symlink the binaries installed via MacPorts in /opt/local/bin/
to /usr/bin/ with ...

.. code-block:: bash

    sudo ln -s /opt/local/bin/tesseract /usr/bin/tesseract

... alternatively set the paths in the ``settings/locals.py``

.. code-block:: python

    LIBREOFFICE_PATH = '/Applications/LibreOffice.app/Contents/MacOS/soffice'

Or Use Homebrew
~~~~~~~~~~~~~~~

With Homebrew installed run the command:

.. code-block:: bash

    brew install python gcc tesseract unpaper poppler libpng postgresql

Set the Binary paths
********************

Mayan EDMS by default will look in /usr/bin/ for the binary files it needs
so either you can symlink the binaries installed via brew in /usr/local/bin/
to /usr/bin/ with ...

.. code-block:: bash

    sudo ln -s /usr/local/bin/tesseract /usr/bin/tesseract  && \
    sudo ln -s /usr/local/bin/unpaper /usr/bin/unpaper && \
    sudo ln -s /usr/local/bin/pdftotext /usr/bin/pdftotext && \
    sudo ln -s /usr/local/bin/gs /usr/bin/gs

... alternatively set the paths in the ``settings/locals.py``

.. code-block:: python

    LIBREOFFICE_PATH = '/Applications/LibreOffice.app/Contents/MacOS/soffice'

Actual project installation
===========================

Initialize a ``virtualenv`` to deploy the project:

.. code-block:: bash

    virtualenv venv
    source venv/bin/activate
    pip install mayan-edms

By default Mayan EDMS will create a single file SQLite_ database, which makes
it very easy to start using Mayan EDMS. Populate the database with the
project's schema doing:

.. code-block:: bash

    mayan-edms.py initialsetup
    mayan-edms.py runserver

Point your browser to http://127.0.0.1:8000. If everything was installed
correctly you should see the login screen and panel showing a randomly generated
admin password.

Background tasks and scheduled tasks will not run when using the test server.

The ``runserver`` command is only meant for testing, do not use in a production
server.

Note that the default IP address, 127.0.0.1, is not accessible from other
machines on your network. To make your test server viewable to other
machines on the network, use its own IP address (e.g. 192.168.2.1) or 0.0.0.0 or :: (with IPv6 enabled).

You can provide an IPv6 address surrounded by brackets (e.g. [200a::1]:8000). This will automatically enable IPv6 support.

Production use
==============

After making sure everything is running correctly, stop the ``runserver`` command.
Deploy Mayan EDMS using the webserver of your preference. For more information
on deployment instructions and examples, checkout Django's official documentation
on the topic https://docs.djangoproject.com/en/1.7/howto/deployment/
For a simple production deployment setup follow the instructions in the
:doc:`deploying` chapter.


.. _Debian: http://www.debian.org/
.. _Django: http://www.djangoproject.com/
.. _Download: https://github.com/mayan-edms/mayan-edms/archives/master
.. _Python: http://www.python.org/
.. _SQLite: https://www.sqlite.org/
.. _Ubuntu: http://www.ubuntu.com/
.. _virtualenv: http://www.virtualenv.org/en/latest/index.html
