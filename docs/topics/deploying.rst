=========
Deploying
=========

OS "bare metal"
===============

Like other Django based projects Mayan EDMS can be deployed in a wide variety
of ways. The method provided below is only a bare minimum example.
These instructions are independent of the instructions mentioned in the
:doc:`installation` chapter but assume you have already made a test install to
test the compatibility of your operating system. These instruction are for
Ubuntu 15.04.

Switch to superuser::

    sudo -i

Install all system dependencies::

    apt-get install nginx supervisor redis-server postgresql \
    libpq-dev libjpeg-dev libmagic1 libpng-dev libreoffice \
    libtiff-dev gcc ghostscript gpgv python-dev python-virtualenv \
    tesseract-ocr unpaper poppler-utils -y

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

Restart the services::

    /etc/init.d/nginx restart
    /etc/init.d/supervisor restart

Docker
======

Deploy the Docker image stack::

    docker run --name postgres -e POSTGRES_DB=mayan -e POSTGRES_USER=mayan -e POSTGRES_PASSWORD=mysecretpassword -v /var/lib/postgresql/data -d postgres
    docker run --name redis -d redis
    docker run --name mayan-edms -p 80:80 --link postgres:postgres --link redis:redis -e POSTGRES_DB=mayan -e POSTGRES_USER=mayan -e POSTGRES_PASSWORD=mysecretpassword -v /usr/local/lib/python2.7/dist-packages/mayan/media -d mayanedms/monolithic

After the Mayan EDMS container finishes initializing (about 5 minutes), it will
be available by browsing to http://127.0.0.1. You can inspect the initialization
with::

    docker logs mayan-edms


Docker Compose
==============

Create a file named ``environment`` with the following content::

    POSTGRES_DB=mayan
    POSTGRES_PASSWORD=mayanpassword
    POSTGRES_USER=mayan

Create a file named ``docker-compose.yml`` with the content::

    postgres:
        env_file:
            - ./environment
        image: postgres
        volumes:
            - /var/lib/postgresql/data

    redis:
        image: redis

    mayan-edms:
        env_file:
            - ./environment
        image: mayanedms/monolithic
        links:
            - postgres
            - redis
        ports:
            - "80:80"
        volumes:
            - /usr/local/lib/python2.7/dist-packages/mayan/media

Launch the entire stack (Postgres, Redis, and Mayan EDMS) using::

    docker-compose -f docker-compose.yml -p mayanedms up -d

After the Mayan EDMS container finishes initializing (about 5 minutes), it will
be available by browsing to http://127.0.0.1. You can inspect the initialization
with::

    docker logs mayanedms_mayan-edms_1

Vagrant
=======
Make sure you have Vagrant and a provider properly installed as per
https://docs.vagrantup.com/v2/installation/index.html
Clone the repository and execute::

    vagrant up production

