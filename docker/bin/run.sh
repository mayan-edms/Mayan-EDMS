#!/bin/bash

# Launch NGINX daemon
nginx

# Launch the workers
mayan-edms.py celery worker --settings=mayan.settings.production -Ofair -l ERROR -B -D

# Launch uWSGI in foreground
/usr/local/bin/uwsgi --ini /docker/conf/uwsgi/uwsgi.ini
