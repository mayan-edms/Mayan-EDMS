from mayan.settings.includes.common import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mayan',
        'USER': 'mayan',
        'PASSWORD': DBPASSWORD,
        'HOST': '',
        'PORT': ''}}