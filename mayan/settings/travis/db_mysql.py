from __future__ import absolute_import

from .. import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mayan_edms',
        'USER': 'travis',
    }
}
