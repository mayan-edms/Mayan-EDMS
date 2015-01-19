from __future__ import absolute_import, unicode_literals

from .. import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mayan_edms',
        'USER': 'travis',
    }
}
