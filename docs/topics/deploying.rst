=========
Deploying
=========

Like other Django based projects **Mayan EDMS** can be deployed in a wide variety
of ways. The method provided below is only provided as a bare minimum example.
These instructions asume you installed **Mayan EDMS** as mentioned in the
Installation chapter.

Install the system dependencies:

    sudo apt-get install nginx supervisor redis-server

Switch and activate the `virtualenv` where you installed **Mayan EDMS**. Install
the Python client for redis:

    pip install redis

Install the Python application server gunicorn:

    pip install gunicorn

Update the settings/local.py file:

    BROKER_URL = 'redis://127.0.0.1:6379/0'
    CELERY_ALWAYS_EAGER = False
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

