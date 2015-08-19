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
        'django_gpg': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARNING',
        },
        'document_indexing': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARNING',
        },
        'document_signatures': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARNING',
        },
        'documents': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARNING',
        },
        'dynamic_search': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARNING',
        },
        'folders': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARNING',
        },
        'lock_manager': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARNING',
        },
        'ocr': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARNING',
        },
        'permissions': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARNING',
        },
        'sources': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARNING',
        },
        'tags': {
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
