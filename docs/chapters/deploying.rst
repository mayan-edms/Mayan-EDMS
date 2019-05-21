******************
Direct deployments
******************

Mayan EDMS should be deployed like any other Django_ project and
preferably using virtualenv_. Below are some ways to deploy and use Mayan EDMS.
Do not use more than one method.

Being a Django_ and a Python_ project, familiarity with these technologies is
recommended to better understand why Mayan EDMS does some of the things it
does.

Compilers and development libraries will be installed to compile runtime
libraries. LibreOffice and Poppler utils will also be installed as they are
used to convert document files. Supervisor (http://supervisord.org/), a
Process Control System, will be used to monitor and keep all Mayan processes
running.


Basic deployment
================
This setup uses less memory and CPU resources at the expense of some speed.
For another setup that offers more performance and scalability refer to the
`Advanced deployment`_ below.

1. Install binary dependencies:
-------------------------------
   If using a Debian_ or Ubuntu_ based Linux distribution, get the executable
   requirements using::

       sudo apt-get install g++ gcc ghostscript gnupg1 graphviz libfuse2 \
       libjpeg-dev libmagic1 libpq-dev libpng-dev libreoffice libtiff-dev \
       poppler-utils postgresql python-dev python-virtualenv redis-server \
       sane-utils supervisor tesseract-ocr zlib1g-dev -y

   .. note::

       Platforms with the ARM CPU might also need additional requirements.
       ::

           apt-sudo get libffi-dev libssl-dev -y


2. Create the user account for the installation:
------------------------------------------------
   This will create an unpriviledge user account that is also unable to login.
   ::

       sudo adduser mayan --disabled-password --disabled-login --no-create-home --gecos ""


3. Create the parent directory where the project will be deployed:
------------------------------------------------------------------
   ``/opt/`` is a good choice as it is meant is for "software and add-on packages
   that are not part of the default installation". (https://www.tldp.org/LDP/Linux-Filesystem-Hierarchy/html/opt.html)
   ::

       sudo mkdir /opt


4. Create the Python virtual environment:
-----------------------------------------
   This will keep all the Python packages installed here isolated from the rest
   of the Pythoon packages in the system.
   ::

       sudo virtualenv /opt/mayan-edms


5. Make the mayan user the owner of the installation directory:
---------------------------------------------------------------
   ::

       sudo chown mayan:mayan /opt/mayan-edms -R


6. Install Mayan EDMS from PyPI:
--------------------------------
   ::

       sudo -u mayan /opt/mayan-edms/bin/pip install --no-cache-dir --no-use-pep517 mayan-edms


7. Install the Python client for PostgreSQL and Redis:
------------------------------------------------------
   ::

       sudo -u mayan /opt/mayan-edms/bin/pip install --no-cache-dir --no-use-pep517 psycopg2==2.7.3.2 redis==2.10.6

   .. note::

       Platforms with the ARM CPU might also need additional requirements.
       ::

           sudo -u mayan /opt/mayan-edms/bin/pip install --no-cache-dir --no-use-pep517 psutil==5.6.2


8. Create the database for the installation:
--------------------------------------------
   ::

       sudo -u postgres psql -c "CREATE USER mayan WITH password 'mayanuserpass';"
       sudo -u postgres createdb -O mayan mayan


9. Initialize the project:
--------------------------
   This step will create all the database structures, download static media files
   like JavaScript libraries and HTML frameworks, and create and initial admin
   account with a random password.

   .. note::

       For simplicity, the ``MAYAN_MEDIA_ROOT`` folder is set to be a subfolder
       of the installation. If you want to keep your files separated from
       the installation files, change the value of the ``MAYAN_MEDIR_ROOT``
       variable in this and all subsequent steps. Be sure to first create the
       folder and give owership of it to the ``mayan`` user with the ``chown``
       command.

   .. warning::

       If this step is interrupted, even if it is later resumed, will
       cause the automatic admin user to no be created in some cases. Make sure all
       environment variable and values are correct. If this happens, refer to the
       troubleshooting chapters: :ref:`troubleshooting-autoadmin-account` and
       :ref:`troubleshooting-admin-password`.

   ::

       sudo -u mayan MAYAN_DATABASE_ENGINE=django.db.backends.postgresql MAYAN_DATABASE_NAME=mayan \
       MAYAN_DATABASE_PASSWORD=mayanuserpass MAYAN_DATABASE_USER=mayan \
       MAYAN_DATABASE_HOST=127.0.0.1 MAYAN_MEDIA_ROOT=/opt/mayan-edms/media \
       /opt/mayan-edms/bin/mayan-edms.py initialsetup


10. Collect the static files:
-----------------------------
    This step merges and compressed static media files so they can be served more
    effectively.

    ::

        sudo -u mayan MAYAN_MEDIA_ROOT=/opt/mayan-edms/media \
        /opt/mayan-edms/bin/mayan-edms.py preparestatic --noinput


11. Create the supervisor file at ``/etc/supervisor/conf.d/mayan.conf``:
------------------------------------------------------------------------
    ::

        MAYAN_DATABASE_ENGINE=django.db.backends.postgresql MAYAN_DATABASE_NAME=mayan \
        MAYAN_DATABASE_PASSWORD=mayanuserpass MAYAN_DATABASE_USER=mayan \
        MAYAN_DATABASE_HOST=127.0.0.1 MAYAN_MEDIA_ROOT=/opt/mayan-edms/media \
        /opt/mayan-edms/bin/mayan-edms.py platformtemplate supervisord > /etc/supervisor/conf.d/mayan.conf


12. Configure Redis:
--------------------
    Configure Redit to discard data when it runs out of memory, not save its
    database and only keep 1 database:
    ::

        echo "maxmemory-policy allkeys-lru" >> /etc/redis/redis.conf
        echo "save \"\"" >> /etc/redis/redis.conf
        echo "databases 1" >> /etc/redis/redis.conf
        systemctl restart redis

13. Enable and restart the services [1_]:
-----------------------------------------
    ::

        systemctl enable supervisor
        systemctl restart supervisor


14. Cleaning up:
----------------
    The following operating system dependencies are only needed during
    installation and can be removed.
    ::

        apt-get remove --purge libjpeg-dev libpq-dev libpng-dev libtiff-dev zlib1g-dev


.. _deployment_advanced:

Advanced deployment
===================

This variation uses RabbitMQ as the message broker. RabbitMQ consumes more
memory but scales to thousands of messages per second. RabbitMQ messages are also
persistent by default, this means that pending tasks are not lost in the case
of a restart or power failure. The Gunicorn workers are increased to 3.


1. Install RabbitMQ:
--------------------

   If using a Debian_ or Ubuntu_ based Linux distribution, get the executable
   requirements using::

       sudo apt-get install rabbitmq-server -y


2. Install the Python client for RabbitMQ:
------------------------------------------
   ::

       sudo -u mayan /opt/mayan-edms/bin/pip install --no-cache-dir --no-use-pep517 librabbitmq==2.0.0


3. Create the RabbitMQ user and vhost:
--------------------------------------
   ::

       sudo rabbitmqctl add_user mayan mayanrabbitmqpassword
       sudo rabbitmqctl add_vhost mayan
       sudo rabbitmqctl set_permissions -p mayan mayan ".*" ".*" ".*"


4. Edit the supervisor file at ``/etc/supervisor/conf.d/mayan.conf``:
---------------------------------------------------------------------
   Replace (paying attention to the comma at the end)::

       MAYAN_BROKER_URL="redis://127.0.0.1:6379/0",

   with::

       MAYAN_BROKER_URL="amqp://mayan:mayanuserpass@localhost:5672/mayan",

   increase the number of Gunicorn workers to 3 in the line (``-w 2`` section)::

       command = /opt/mayan-edms/bin/gunicorn -w 2 mayan.wsgi --max-requests 1000 --max-requests-jitter 50 --worker-class gevent --bind 0.0.0.0:8000 --timeout 120

   remove the concurrency limit (or increase it) of the fast worker (remove ``--concurrency=1``).


5. Restart the services:
------------------------
   ::

       supervisorctl restart all




[1]: https://bugs.launchpad.net/ubuntu/+source/supervisor/+bug/1594740

.. _Debian: https://www.debian.org/
.. _Django: https://www.djangoproject.com/
.. _Python: https://www.python.org/
.. _SQLite: https://www.sqlite.org/
.. _Ubuntu: http://www.ubuntu.com/
.. _virtualenv: http://www.virtualenv.org/en/latest/index.html
.. _1: https://bugs.launchpad.net/ubuntu/+source/supervisor/+bug/1594740
