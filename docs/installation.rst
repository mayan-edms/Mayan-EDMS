============
Installation
============
**Mayan EDMS** should be installed like any other Django project and preferably using ``virtualenv``.

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

    $ ./manage.py syncdb 
    
Collect the static files of the project into the ``static`` folder for serving via a webserver::

    $ ./manage.py collectstatic

After that deploy it using the webserver of your preference.  If your are using Apache_, a sample site file is included under the contrib directory.

.. _Apache: https://www.apache.org/
.. _Debian: http://www.debian.org/
.. _Ubuntu: http://www.ubuntu.com/
.. _Download: https://github.com/rosarior/mayan/archives/master
