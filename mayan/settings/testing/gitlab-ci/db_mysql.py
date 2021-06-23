from ...literal import (
    DEFAULT_DATABASE_NAME, DEFAULT_DATABASE_PASSWORD, DEFAULT_DATABASE_USER
)

from .base import *  # NOQA

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DEFAULT_DATABASE_NAME,
        'USER': DEFAULT_DATABASE_USER,
        'PASSWORD': DEFAULT_DATABASE_PASSWORD,
        'HOST': 'mysql'
    }
}
