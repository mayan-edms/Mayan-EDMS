from mayan.settings.includes.common import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['.crossculturalconsult.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mayan',
        'USER': 'mayan',
        'PASSWORD': DBPASSWORD,
        'HOST': '',
        'PORT': ''}}