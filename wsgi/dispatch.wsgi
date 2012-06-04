import os
import sys
import site
import platform

sys.stdout = sys.stderr

ve_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'lib/python%s/site-packages' % platform.python_version()[:3]))

# Add the virtual Python environment site-packages directory to the path
site.addsitedir(ve_path)

# put the Django project on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.insert(0, ve_path)

# Avoid ``[Errno 13] Permission denied: '/var/www/.python-eggs'`` messages
os.environ['PYTHON_EGG_CACHE'] = '/tmp'
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core.handlers.wsgi import WSGIHandler

application = WSGIHandler()
