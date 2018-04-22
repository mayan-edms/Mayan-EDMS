from __future__ import absolute_import, unicode_literals

from .. import *  # NOQA

COMMON_PRODUCTION_ERROR_LOG_PATH = '/tmp'
INSTALLED_APPS += ('test_without_migrations',)
TEMPLATES[0]['OPTIONS']['loaders'] = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
