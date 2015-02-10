from __future__ import unicode_literals

from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mayan_edms',
        'USER': 'postgres',
    }
}
