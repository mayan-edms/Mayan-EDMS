"""Configuration options for the storage app"""
import os

from django.conf import settings

from smart_settings.api import register_settings

register_settings(
    namespace=u'storage',
    module=u'storage.conf.settings',
    settings=[
        {'name': u'GRIDFS_HOST', 'global_name': u'STORAGE_GRIDFS_HOST', 'default': u'localhost'},
        {'name': u'GRIDFS_PORT', 'global_name': u'STORAGE_GRIDFS_PORT', 'default': 27017},
        {'name': u'GRIDFS_DATABASE_NAME', 'global_name': u'STORAGE_GRIDFS_DATABASE_NAME', 'default': u'document_storage'},
        {'name': u'FILESTORAGE_LOCATION', 'global_name': u'STORAGE_FILESTORAGE_LOCATION', 'default': os.path.join(settings.MEDIA_ROOT, u'document_storage'), 'exists': True},
    ]
)
