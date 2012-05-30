============
Installation
============

Local or managed server
-----------------------

**Mayan EDMS** should be deployed_ like any other Django_ project and preferably using virtualenv_.

If using a Debian_ or Ubuntu_ based Linux distribution getting the executable requirements is as easy as::

	$ apt-get install tesseract-ocr unpaper python-virtualenv ghostscript libjpeg-dev libpng-dev poppler-utils -y
    
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
    
If using PostgreSQL, enter the following::

    $ apt-get install python-dev libpq-dev gcc-y
    $ pip install pip install psycopg2

Populate the database with the project's schema doing::

    $ ./manage.py syncdb --migrate
    
Collect the static files of the project into the ``static`` folder for serving via a webserver::

    $ ./manage.py collectstatic

To test your installation, create a file called settings_local.py with the following content::

    DEBUG=True
    DEVELOPMENT=True

Execute Django’s development server using the ``runserver`` command to launch a local instance of Mayan EDMS::

    $ ./manager.py runserver

Point your browser to http://127:0.0.1:8000, if everything was installed correctly you should see the login screen.  After making sure everything is running correctly, stop the runserver command, delete the settings_local.py and deploy Mayan EDMS using the webserver of your preference. If your are using Apache_, a sample site file is included under the contrib directory.


Webfaction
----------

To install **Mayan EDMS** on Webfaction_, follow these steps:

1. Create a new database:

  * Enter the following selections:

    * Type:* ``Mysql``
    * Name:* ``<username>_mayan``
    * Encoding:* ``utf-8``

  * Anotate the provided password.

2. Create a new app:
    
  * Enter the following in the textbox:
    
    * Name:* ``mayan_app``
    * App category:* ``mod_wsgi``
    * App type:* ``mod_wsgi 3.3/Python 2.7``

3. Login via ssh, and execute::

    $ easy_install-2.7 virtualenv
    $ cd ~/webapps/mayan_app
    $ virtualenv --no-site-packages mayan
    $ cd mayan
    $ git clone git://github.com/rosarior/mayan.git
    $ cd mayan
    $ source ../bin/activate
    $ pip install -r requirements/production.txt

4. Install the Python MySQL database driver::

    $ pip install MySQL-python

5. Create a settings_local.py file, and paste into it the following::

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', 
            'NAME': '<username>_mayan',
            'USER': '<username>_mayan',
            'PASSWORD': '<database password from step 1>',
            'HOST': '',
            'PORT': '',
        }
    }

6. Create the database schema::

    $ ./manage.py syncdb --migrate

7. Collect the static files of the apps::

    $ ./manage.py collectstatic -l --noinput

8. Create a new app:

  * Enter the following:
    
    * Name:* ``mayan_static``
    * App category:* ``Symbolic link``
    * App type:* ``Symbolic link to static-only app``
    * Extra info: ``/home/<username>/webapps/mayan_app/mayan/mayan/static``

9. Create the website:

  * Name: ``mayan_edms``
  * Choose a subdomain
  * Under ``Site apps:`` enter the following selections: 
    
    * App #1
        
      * App:* ``mayan_app``
      * URL path (ex: '/' or '/blog'):* ``/``
            
    * App #2
        
      * App:* ``mayan_static``
      * URL path (ex: '/' or '/blog'):* ``/mayan-static``

10. Edit the file ``~/webapps/mayan_app/apache2/conf/httpd.conf``:
    
  * Disable the ``DirectoryIndex`` line and the ``DocumentRoot`` line.
  * Add the following line::
        
      WSGIScriptAlias / /home/<username>/webapps/mayan_app/mayan/mayan/wsgi/dispatch.wsgi
 
  * Tune your WSGI process to only use 2 workers (as explained here: `Reducing mod_wsgi Memory Consumption`_)
    to keep the memory usage under the basic 256MB of RAM provided or upgrade your plan to 512MB,
    the line that controls the amount of workers launched is::
  
      WSGIDaemonProcess mayan_app processes=5 python-path=/home/<username>/webapps/mayan_app/lib/python2.7 threads=1
      
    change it to::
    
      WSGIDaemonProcess mayan_app processes=2 python-path=/home/<username>/webapps/mayan_app/lib/python2.7 threads=1


11. Restart your apache instance:

  * Execute::

     apache2/bin/restart

 
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
.. _Django: http://www.djangoproject.com/


.. _Apache: https://www.apache.org/
.. _Debian: http://www.debian.org/
.. _Ubuntu: http://www.ubuntu.com/
.. _Download: https://github.com/rosarior/mayan/archives/master
.. _Webfaction: http://www.webfaction.com
.. _deployed: https://docs.djangoproject.com/en/1.3/howto/deployment/
.. _virtualenv: http://www.virtualenv.org/en/latest/index.html
.. _`Reducing mod_wsgi Memory Consumption`: http://docs.webfaction.com/software/mod-wsgi.html#mod-wsgi-reducing-memory-consumption
