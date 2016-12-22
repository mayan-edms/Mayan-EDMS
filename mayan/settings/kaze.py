from __future__ import absolute_import, unicode_literals

from .production import *  # NOQA

if not BROKER_URL:
    BROKER_URL = 'redis://127.0.0.1:6379/0'

if not CELERY_RESULT_BACKEND:
    CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'


