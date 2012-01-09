============
Installation
============

Local or managed server
-----------------------

**Mayan EDMS** should be deployed_ like any other Django_ project and preferably using virtualenv_.

If using a Debian_ or Ubuntu_ based Linux distribution getting the executable requirements is as easy as::

	$ apt-get install tesseract-ocr unpaper python-virtualenv ghostscript -y
    
To initialize a ``virtualenv`` to deploy the project do::

	$ virtualenv --no-site-packages mayan
    
Download_ and decompress the latest version of **Mayan EDMS**::

	$ cd mayan
	$ tar -xvzf mayan.tar.gz
    
Or clone the latest development version straight from github::

	$ cd mayan
	$ git clone git://github.com/rosarior/mayan.git

To install the python dependencies ``easy_install`` can be used, however for easier retrieval a production dependencies file is included, to use it execute::

	$ cd mayan
	$ source ../bin/activate
	$ pip install -r requirements/production.txt

Create the database that will hold the data. Install any corresponding python database drivers. Update the settings.py file with you database settings.
If using the ``MySQL`` database manager, use the following commands::

    $ apt-get install python-dev libmysqlclient-dev gcc -y
    $ pip install MySQL-python

Populate the database with the project's schema doing::

    $ ./manage.py syncdb --migrate
    
Collect the static files of the project into the ``static`` folder for serving via a webserver::

    $ ./manage.py collectstatic

After that deploy it using the webserver of your preference.  If your are using Apache_, a sample site file is included under the contrib directory.

Webfaction
----------

To install **Mayan EDMS** on Webfaction_, follow these steps:

#. Create a new database:

    * Enter the following selections:

        * Type:* ``Mysql``
        * Name:* ``<username>_mayan``
        * Encoding:* ``utf-8``

    * Anotate the provided password.

#. Create a new app:
    
    * Enter the following in the textbox:
    
        * Name:* ``mayan``
        * App category:* ``mod_wsgi``
        * App type:* ``mod_wsgi 3.3/Python 2.7``

#. Login via ssh, and execute::

    $ easy_install-2.7 virtualenv
    $ cd ~/webapps/mayan_app
    $ virtualenv --no-site-packages mayan
    $ cd mayan
    $ git clone git://github.com/rosarior/mayan.git
    $ cd mayan
    $ source ../bin/activate
    $ pip install -r requirements/production.txt

#. Install the Python MySQL database driver::

    $ pip install MySQL-python

#. Create a settings_local.py file, and paste into it the following::

    $ DATABASES = {
    $     'default': {
    $         'ENGINE': 'django.db.backends.mysql', 
    $         'NAME': '<username>_mayan',
    $         'USER': '<username>_mayan',
    $         'PASSWORD': '<database password from step 1>',
    $         'HOST': '',
    $         'PORT': '',
    $     }
    $ }

#. Create the database schema (during this step two errors will appears about failling to install indexes on ``documents.Document`` and ``documents.DocumentPage`` models, ignore them for now)::

    $ ./manage.py syncdb

#. Collect the static files of the apps::

    $ ./manage.py collectstatic -l --noinput

#. Create a new app:

    * Enter the following:
    
        * Name:* ``mayan_static``
        * App category:* ``Symbolic link``
        * App type:* ``Symbolic link to static-only app``
        * Extra info: ``/home/<username>/webapps/mayan_app/mayan/mayan/static``

#. Create the website:

    * Name: ``mayan_edms``
    * Choose a subdomain
    * Under ``Site apps:`` enter the following selections: 
    
        * App #1
        
            * App:* ``mayan_app``
            * URL path (ex: '/' or '/blog'):* ``/``
            
        * App #2
        
            * App:* ``mayan_static``
            * URL path (ex: '/' or '/blog'):* ``/mayan-static``

#. Edit the file ``~/webapps/mayan_app/apache2/conf/httpd.conf``:
    
    * Disable the ``DirectoryIndex`` line and the ``DocumentRoot`` line
    * Add the following line::
        
        WSGIScriptAlias / /home/<username>/webapps/mayan_app/mayan/mayan/wsgi/dispatch.wsgi

DjangoZoom
----------
For instructions on how to deploy **Mayan EDMS** on DjangoZoom, watch the screencast:

"Deploying Mayan EDMS on DjangoZoom.net" available on Youtube_


.. _`vendor lock-in`: https://secure.wikimedia.org/wikipedia/en/wiki/Vendor_lock-in
.. _Python: http://www.python.org/
.. _Django: http://www.djangoproject.com/
.. _OCR: https://secure.wikimedia.org/wikipedia/en/wiki/Optical_character_recognition
.. _`Open source`: https://secure.wikimedia.org/wikipedia/en/wiki/Open_source
.. _DjangoZoom: http://djangozoom.com/
.. _Youtube: http://bit.ly/mayan-djangozoom


.. _Apache: https://www.apache.org/
.. _Debian: http://www.debian.org/
.. _Ubuntu: http://www.ubuntu.com/
.. _Download: https://github.com/rosarior/mayan/archives/master
.. _Webfaction: http://www.webfaction.com
.. _deployed: https://docs.djangoproject.com/en/1.3/howto/deployment/
.. _Django: https://www.djangoproject.com
.. _virtualenv: http://www.virtualenv.org/en/latest/index.html
