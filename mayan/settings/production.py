from .includes.common import *

from .includes.common import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['.crossculturalconsult.com']


###################
# DEPLOY SETTINGS #
###################

GUNICORN_BIND = "127.0.0.1:8731"
PROCESS_USER = 'mayan'
PROCESS_NAME = 'mayan_production'
SITE_TITLE = 'Mayan CCCS'
SITE_TAGLINE = None
VIRTUALENV = 'production'