from __future__ import absolute_import, unicode_literals

from ..base import *  # NOQA


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
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
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'intermediate'
        }
    },
    'loggers': {
        'acls': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARNING',
        },
        'converter': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARNING',
        },
        'documents': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARNING',
        },
        'document_indexing': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARNING',
        },
        'ocr': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARNING',
        },
    }
}


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader'
)
