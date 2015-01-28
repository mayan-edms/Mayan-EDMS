from __future__ import absolute_import, unicode_literals

from .. import *

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
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'intermediate'
        }
    },
    'loggers': {
        'documents': {
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
        },
        'converter': {
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
        },
        'ocr': {
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
        },
    }
}
