from .base import *  # NOQA

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mayan_edms',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'postgres',
    }
}
