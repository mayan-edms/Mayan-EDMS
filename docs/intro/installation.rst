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

Initialize a ``virtualenv`` to deploy the project::

    $ virtualenv --no-site-packages venv
    $ source venv/bin/activate

Download_ and decompress the latest version of **Mayan EDMS**::

    $ cd venv
    $ tar -xvzf mayan.tar.gz

Or clone the latest development version straight from github::

    $ cd venv
    $ git clone https://github.com/mayan-edms/mayan-edms.git

To install the python dependencies ``easy_install`` can be used, however for easier retrieval a production dependencies file is included, to use it execute::

    $ cd mayan-edms
    $ pip install -r requirements.txt

By default **Mayan EDMS** will create a single file SQLite_ database which makes is very easy to start using **Mayan EDMS**.
Populate the database with the project's schema doing::

    $ ./manage.py syncdb --migrate --noinput


To test your installation, execute Django’s development server using the ``runserver`` command to launch a local instance of **Mayan EDMS**::

    $ ./manage.py runserver

Point your browser to http://127:0.0.1:8000, if everything was installed
correctly you should see the login screen and panel showing a randomly generated admin password.


Production use
--------------

After making sure everything is running correctly, stop the runserver command.
Deploy **Mayan EDMS** using the webserver of your preference. For more information
on deployment instructions and examples checkout Django's official documentation
on the topic https://docs.djangoproject.com/en/1.6/howto/deployment/


Other database managers
-----------------------

If you want to use a database manager other than SQLite_ install any
corresponding python database drivers and create a settings_local.py file
with the corresponding database settings as shown here: https://docs.djangoproject.com/en/1.6/ref/settings/#std:setting-DATABASES


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
