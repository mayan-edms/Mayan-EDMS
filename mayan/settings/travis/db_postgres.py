from __future__ import absolute_import

from .. import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mayan_edms',
        'USER': 'postgres',
    }
}
