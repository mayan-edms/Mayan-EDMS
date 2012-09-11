from __future__ import absolute_import

import os

from django.utils.translation import ugettext_lazy as _
from django.conf import settings as django_settings

from smart_settings import LocalScope

from .icons import icon_storage

label = _(u'Storage')
description = _(u'Handles actual storage of files by means of specialized backends.')
icon = icon_storage
dependencies = ['app_registry']
settings = [
    {
        'name': 'GRIDFS_HOST',
        'default': u'localhost',
        'scopes': [LocalScope()]
    },
    {
        'name': 'GRIDFS_PORT',
        'default': 27017,
        'scopes': [LocalScope()]
    },
    {
        'name': 'GRIDFS_DATABASE_NAME',
        'default': 'document_storage',
        'scopes': [LocalScope()]
    },
    {
        'name': 'FILESTORAGE_LOCATION',
        'default': os.path.join(django_settings.PROJECT_ROOT, u'document_storage'),
        'exists': True,
        'scopes': [LocalScope()]
    },
]
