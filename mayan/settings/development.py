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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(name)s %(process)d %(thread)d %(message)s'
        },
        'intermediate': {
            'format': '%(name)s <%(process)d> [%(levelname)s] "%(funcName)s() %(message)s"'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'intermediate'
        }
    },
    'loggers': {
        'documents': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'common': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
    }
}

CELERY_EAGER_PROPAGATES_EXCEPTIONS = CELERY_ALWAYS_EAGER
