# sample wsgi file for usage with apache webserver
# mayan installation in a virtualenv /opt/mayan/venv
# apache deployment in /var/www/mayan-edms
import os
import sys
import site
# set up python path to virtual environment
site.addsitedir(‘/opt/mayan/venv/lib/python2.7/site-packages’)
sys.path.append(‘/var/www/mayan-edms’)
os.environ[‘PYTHON_EGG_CACHE’]=’/var/www/django/cache’
#django WSGI specifics
From django.core.handlers.wsgi import WSGIHandler
os.environ[‘DJANGO_SETTING_MODULE’] = ‘mayan.settings.production’
application = WSGIHandler()
