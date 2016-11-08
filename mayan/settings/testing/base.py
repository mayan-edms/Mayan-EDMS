from __future__ import absolute_import, unicode_literals

from ..base import *  # NOQA

INSTALLED_APPS += ('test_without_migrations',)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader'
)
