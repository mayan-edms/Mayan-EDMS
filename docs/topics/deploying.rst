=========
Deploying
=========

Like other Django based projects **Mayan EDMS** can be deployed in a wide variety
of ways. The method provided below is only a bare minimum example.
These instructions asume you installed **Mayan EDMS** as mentioned in the :doc:`installation` chapter.

Install more system dependencies::

    sudo apt-get install nginx supervisor redis-server postgresql

- Postgresql pg_hba.conf
- Postgresql user
- Postgresql database

Switch and activate the `virtualenv` where you installed **Mayan EDMS**. Install
the Python client for redis and uWSGI::

    pip install redis uwsgi

Update the settings/local.py file::

    BROKER_URL = 'redis://127.0.0.1:6379/0'
    CELERY_ALWAYS_EAGER = False
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'


- NGINX site
- SUPERVISOR uwsgi
- SUPERVISOR worker

