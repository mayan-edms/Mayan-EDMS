from __future__ import absolute_import, unicode_literals

from . import *  # NOQA

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader'
)

INSTALLED_APPS += (
    'rosetta',
    'django_extensions',
)

WSGI_AUTO_RELOAD = True

CELERY_EAGER_PROPAGATES_EXCEPTIONS = CELERY_ALWAYS_EAGER
