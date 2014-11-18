============
Installation
============

Ubuntu, Debian or Fedora server
-------------------------------

**Mayan EDMS** should be deployed like any other Django_ project and preferably using virtualenv_.

If using a Debian_ or Ubuntu_ based Linux distribution getting the executable requirements is as easy as::

    $ sudo apt-get install python-dev gcc tesseract-ocr unpaper python-virtualenv ghostscript libjpeg-dev libpng-dev poppler-utils -y

If using a Fedora_ based Linux distribution get the executable requirements using Yum::

    $ sudo yum install -y git gcc tesseract unpaper python-virtualenv ghostscript libjpeg-turbo-devel libpng-devel poppler-util python-devel

Initialize a ``virtualenv`` to deploy the project:

.. code-block:: bash

    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install mayan-edms

By default **Mayan EDMS** will create a single file SQLite_ database, which makes
it very easy to start using **Mayan EDMS**. Populate the database with the project's schema doing:

.. code-block:: bash

    $ mayan-edms.py initialsetup
    $ mayan-edms.py runserver

Point your browser to http://127.0.0.1:8000. If everything was installed
correctly you should see the login screen and panel showing a randomly generated admin password.

Mac OSX
-------

**Mayan EDMS** is dependant on a number of binary packages and the recommended way is
to use a package manager such as `MacPorts <https://www.macports.org/>`_.


Use MacPorts to install binary dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With MacPorts installed run the command:

.. code-block:: bash

    sudo port install python-dev gcc tesseract-ocr unpaper python-virtualenv ghostscript libjpeg-dev libpng-dev poppler-utils

**Mayan EDMS** can use either Pillow, ImageMagick or GraphicsMagick as the backend to
convert images so in addition you can install GraphicsMagick ...

.. code-block:: bash

    sudo port install graphicsmagick

Set the Binary paths
~~~~~~~~~~~~~~~~~~~~

**Mayan EDMS** by default will look in /usr/bin/ for the binary files it needs
so either you can symlink the binaries installed via MacPorts in /opt/local/bin/
to /usr/bin/ with ...

.. code-block:: bash

    sudo ln -s /opt/local/bin/tesseract /usr/bin/tesseract  && \
    sudo ln -s /opt/local/bin/identify /usr/bin/identify && \
    sudo ln -s /opt/local/bin/gs /usr/bin/gs

... alternatively set the paths in the ``settings/locals.py``

.. code-block:: python

    # document converters
    CONVERTER_IM_CONVERT_PATH = '/opt/local/bin/convert'
    IM_IDENTIFY_PATH = '/opt/local/bin/identify'
    GRAPHICS_BACKEND = 'converter.backends.graphicsmagick.GraphicsMagick'
    GM_PATH = '/opt/local/bin/gm'
    LIBREOFFICE_PATH = '/Applications/LibreOffice.app/Contents/MacOS/soffice'

Production use
--------------

To create a custom settings file for **Mayan EDMS**, create a Python (.py) file
in the directory: venv/lib/python2.7/site-packages/mayan/settings/ with the following basic content::

    # my_settings.py

    from __future__ import absolute_import

    from .local import *

    <Your customized settings>

To test your settings launch **Mayan EDMS** using::

    $ mayan-edms runserver --settings=mayan.settings.my_settings

After making sure everything is running correctly, stop the runserver command.
Deploy **Mayan EDMS** using the webserver of your preference. For more information
on deployment instructions and examples checkout Django's official documentation
on the topic https://docs.djangoproject.com/en/1.6/howto/deployment/



Other database managers
-----------------------

If you want to use a database manager other than SQLite_ install any
corresponding python database drivers and add the corresponding database settings
to your settings file (see above) as shown here: https://docs.djangoproject.com/en/1.6/ref/settings/#std:setting-DATABASES


.. _`vendor lock-in`: https://secure.wikimedia.org/wikipedia/en/wiki/Vendor_lock-in
.. _Python: http://www.python.org/
.. _Django: http://www.djangoproject.com/
.. _OCR: https://secure.wikimedia.org/wikipedia/en/wiki/Optical_character_recognition
.. _`Open source`: https://secure.wikimedia.org/wikipedia/en/wiki/Open_source
.. _Django: http://www.djangoproject.com/
.. _Apache: https://www.apache.org/
.. _Debian: http://www.debian.org/
.. _Ubuntu: http://www.ubuntu.com/
.. _Download: https://github.com/mayan-edms/mayan-edms/archives/master
.. _virtualenv: http://www.virtualenv.org/en/latest/index.html
.. _Fedora: http://fedoraproject.org/
.. _SQLite: https://www.sqlite.org/
