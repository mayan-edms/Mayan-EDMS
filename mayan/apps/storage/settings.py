"""Configuration options for the storage app"""
import os

from django.conf import settings

from smart_settings.api import register_settings

register_settings(
    namespace=u'storage',
    module=u'storage.settings',
    settings=[
        {'name': u'FILESTORAGE_LOCATION', 'global_name': u'STORAGE_FILESTORAGE_LOCATION', 'default': os.path.join(settings.MEDIA_ROOT, u'document_storage'), 'exists': True},
    ]
)
