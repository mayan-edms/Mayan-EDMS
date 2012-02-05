import os
import sys
import site

from django.core.handlers.wsgi import WSGIHandler

sys.stdout = sys.stderr

#TODO fix properly
ve_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'lib/python2.7/site-packages'))  # Change python 2.6 to the python version you are using

# Add the virtual Python environment site-packages directory to the path
site.addsitedir(ve_path)

# put the Django project on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.insert(0, ve_path)

# Avoid ``[Errno 13] Permission denied: '/var/www/.python-eggs'`` messages
os.environ['PYTHON_EGG_CACHE'] = '/tmp'
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

application = WSGIHandler()
