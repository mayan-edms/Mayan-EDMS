from __future__ import absolute_import, unicode_literals

from . import *  # NOQA

ALLOWED_HOSTS = ['*']

DEBUG = True

CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = CELERY_ALWAYS_EAGER

if 'rosetta' not in INSTALLED_APPS:
    INSTALLED_APPS += (
        'rosetta',
    )

if 'django_extensions' not in INSTALLED_APPS:
    INSTALLED_APPS += (
        'django_extensions',
    )

TEMPLATES[0]['OPTIONS']['loaders'] = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

WSGI_AUTO_RELOAD = True
