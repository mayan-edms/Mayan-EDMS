from ..production import *  # NOQA

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mayan-staging',
        'HOST': 'localhost',
        'PORT': '5432',
        'PASSWORD': 'mayan-staging',
        'USER': 'mayan-staging'
    }
}

CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
DEBUG = True
