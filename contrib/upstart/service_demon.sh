#!/bin/bash
# Run the gunicorn service

# Make sure we're in the right virtual env and location
source /home/mayan/.virtualenvs/production/bin/activate
source /home/mayan/.virtualenvs/production/bin/postactivate

cd /home/mayan/production

exec gunicorn -c /home/mayan/production/deploy/gunicorn.conf.py mayan.wsgi:application