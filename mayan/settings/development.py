from __future__ import absolute_import

from . import *  # NOQA

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

INTERNAL_IPS = ('127.0.0.1',)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader'
)

INSTALLED_APPS += (
    'rosetta',
    'django_extensions',
)

# Stop debug toolbar patching!
# see https://github.com/django-debug-toolbar/django-debug-toolbar/issues/524
TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.debug',)

WSGI_AUTO_RELOAD = True
