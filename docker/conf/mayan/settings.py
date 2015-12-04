import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_PORT_5432_TCP_ADDR'),
        'PORT': os.environ.get('POSTGRES_PORT_5432_TCP_PORT'),
    }
}

BROKER_URL = 'redis://{}:{}/0'.format(os.environ.get('REDIS_PORT_6379_TCP_ADDR'),  os.environ.get('REDIS_PORT_6379_TCP_PORT'))
CELERY_RESULT_BACKEND = 'redis://{}:{}/0'.format(os.environ.get('REDIS_PORT_6379_TCP_ADDR'),  os.environ.get('REDIS_PORT_6379_TCP_PORT'))
