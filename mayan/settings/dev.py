from mayan.settings.includes.common import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

INTERNAL_IPS = ('127.0.0.1',)

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mayan',
        'USER': 'mayan',
        'PASSWORD': DBPASSWORD,
        'HOST': '',
        'PORT': ''}}

INSTALLED_APPS = INSTALLED_APPS + (
    'rosetta',
    'django_extensions',
    'debug_toolbar')


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader')
TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.debug',)
WSGI_AUTO_RELOAD = True
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
