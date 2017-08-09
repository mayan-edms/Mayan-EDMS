===================
Advanced deployment
===================

Mayan EDMS should be deployed like any other Django_ project and
preferably using virtualenv_. Below are some ways to deploy and use Mayan EDMS.
Do not use more than one method.

Being a Django_ and a Python_ project, familiarity with these technologies is
recommended to better understand why Mayan EDMS does some of the things it
does.

Binary dependencies
===================

Ubuntu
------

If using a Debian_ or Ubuntu_ based Linux distribution, get the executable
requirements using::

    apt-get install graphviz nginx supervisor redis-server postgresql \
    libpq-dev libjpeg-dev libmagic1 libpng-dev libreoffice \
    libtiff-dev gcc ghostscript gnupg python-dev python-virtualenv \
    tesseract-ocr poppler-utils -y

If using Ubuntu 16.10 also install GPG version 1 (as GPG version 2 is the new default for this distribution and not yet supported by Mayan EDMS) ::

    apt-get install gnupg1 -y


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

Alternatively, set the paths in the ``settings/locals.py``

.. code-block:: python

    LIBREOFFICE_PATH = '/Applications/LibreOffice.app/Contents/MacOS/soffice'

Or Use Homebrew
~~~~~~~~~~~~~~~

With Homebrew installed run the command:

.. code-block:: bash

    brew install python gcc tesseract unpaper poppler libpng postgresql

Set the Binary paths
********************

Mayan EDMS by default will look in /usr/bin/ for the binary files it needs.
You can symlink the binaries installed via brew in /usr/local/bin/
to /usr/bin/ with:

.. code-block:: bash

    sudo ln -s /usr/local/bin/tesseract /usr/bin/tesseract  && \
    sudo ln -s /usr/local/bin/unpaper /usr/bin/unpaper && \
    sudo ln -s /usr/local/bin/pdftotext /usr/bin/pdftotext && \
    sudo ln -s /usr/local/bin/gs /usr/bin/gs

Alternatively, set the paths in the ``settings/locals.py``

.. code-block:: python

    LIBREOFFICE_PATH = '/Applications/LibreOffice.app/Contents/MacOS/soffice'


Common steps
------------
Switch to superuser::

    sudo -i

Change to the directory where the project will be deployed::

    cd /usr/share

Create the Python virtual environment for the installation::

    virtualenv mayan-edms

Activate the virtualenv::

    source mayan-edms/bin/activate

Install Mayan EDMS from PyPI::

    pip install mayan-edms

Install the Python client for PostgreSQL, Redis, and uWSGI::

    pip install psycopg2 redis uwsgi

Create the database for the installation::

    sudo -u postgres createuser -P mayan  (provide password)
    sudo -u postgres createdb -O mayan mayan

Create the directory for the log files::

    mkdir /var/log/mayan

Change the current directory to be the one of the installation::

    cd mayan-edms

Make a convenience symbolic link::

    ln -s lib/python2.7/site-packages/mayan .

Create an initial settings file::

    mayan-edms.py createsettings

Append the following to the ``mayan/settings/local.py`` file, paying attention to replace the ``PASSWORD`` value::

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'mayan',
            'USER': 'mayan',
            'PASSWORD': '<password used when creating postgreSQL user>',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

    BROKER_URL = 'redis://127.0.0.1:6379/0'
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

If using Ubuntu 16.10, also add this line to the ``mayan/settings/local.py`` file::

    SIGNATURES_GPG_PATH = '/usr/bin/gpg1'

Migrate the database or initialize the project::

    mayan-edms.py initialsetup

Disable the default NGINX site::

    rm /etc/nginx/sites-enabled/default

Create a ``uwsgi.ini`` file with the following contents::

    [uwsgi]
    chdir = /usr/share/mayan-edms/lib/python2.7/site-packages/mayan
    chmod-socket = 664
    chown-socket = www-data:www-data
    env = DJANGO_SETTINGS_MODULE=mayan.settings.production
    gid = www-data
    logto = /var/log/uwsgi/%n.log
    pythonpath = /usr/share/mayan-edms/lib/python2.7/site-packages
    master = True
    max-requests = 5000
    socket = /usr/share/mayan-edms/uwsgi.sock
    uid = www-data
    vacuum = True
    wsgi-file = /usr/share/mayan-edms/lib/python2.7/site-packages/mayan/wsgi.py

Create the directory for the uWSGI log files::

    mkdir /var/log/uwsgi

Create the NGINX site file for Mayan EDMS, ``/etc/nginx/sites-available/mayan``::

    server {
        listen 80;
        server_name localhost;

        location / {
            include uwsgi_params;
            uwsgi_pass unix:/usr/share/mayan-edms/uwsgi.sock;

            client_max_body_size 30M;  # Increse if your plan to upload bigger documents
            proxy_read_timeout 30s;  # Increase if your document uploads take more than 30 seconds
        }

        location /static {
            alias /usr/share/mayan-edms/mayan/media/static;
            expires 1h;
        }

        location /favicon.ico {
            alias /usr/share/mayan-edms/mayan/media/static/appearance/images/favicon.ico;
            expires 1h;
        }
    }

Enable the NGINX site for Mayan EDMS::

    ln -s /etc/nginx/sites-available/mayan /etc/nginx/sites-enabled/

Create the supervisor file for the uWSGI process, ``/etc/supervisor/conf.d/mayan-uwsgi.conf``::

    [program:mayan-uwsgi]
    command = /usr/share/mayan-edms/bin/uwsgi --ini /usr/share/mayan-edms/uwsgi.ini
    user = root
    autostart = true
    autorestart = true
    redirect_stderr = true

Create the supervisor file for the Celery worker, ``/etc/supervisor/conf.d/mayan-celery.conf``::

    [program:mayan-worker]
    command = /usr/share/mayan-edms/bin/python /usr/share/mayan-edms/bin/mayan-edms.py celery --settings=mayan.settings.production worker -Ofair -l ERROR
    directory = /usr/share/mayan-edms
    user = www-data
    stdout_logfile = /var/log/mayan/worker-stdout.log
    stderr_logfile = /var/log/mayan/worker-stderr.log
    autostart = true
    autorestart = true
    startsecs = 10
    stopwaitsecs = 10
    killasgroup = true
    priority = 998

    [program:mayan-beat]
    command = /usr/share/mayan-edms/bin/python /usr/share/mayan-edms/bin/mayan-edms.py celery --settings=mayan.settings.production beat -l ERROR
    directory = /usr/share/mayan-edms
    user = www-data
    numprocs = 1
    stdout_logfile = /var/log/mayan/beat-stdout.log
    stderr_logfile = /var/log/mayan/beat-stderr.log
    autostart = true
    autorestart = true
    startsecs = 10
    stopwaitsecs = 1
    killasgroup = true
    priority = 998

Collect the static files::

    mayan-edms.py collectstatic --noinput

Make the installation directory readable and writable by the webserver user::

    chown www-data:www-data /usr/share/mayan-edms -R

Enable and restart the services [1_]::

    systemctl enable supervisor
    systemctl restart supervisor
    systemctl restart nginx

[1]: https://bugs.launchpad.net/ubuntu/+source/supervisor/+bug/1594740

.. _Debian: http://www.debian.org/
.. _Django: http://www.djangoproject.com/
.. _Python: http://www.python.org/
.. _SQLite: https://www.sqlite.org/
.. _Ubuntu: http://www.ubuntu.com/
.. _virtualenv: http://www.virtualenv.org/en/latest/index.html
.. _1: https://bugs.launchpad.net/ubuntu/+source/supervisor/+bug/1594740
