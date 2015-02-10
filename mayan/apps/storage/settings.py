from __future__ import unicode_literals

import os

from django.conf import settings

from smart_settings.api import register_settings

register_settings(
    namespace='storage',
    module='storage.settings',
    settings=[
        {'name': 'FILESTORAGE_LOCATION', 'global_name': 'STORAGE_FILESTORAGE_LOCATION', 'default': os.path.join(settings.MEDIA_ROOT, 'document_storage'), 'exists': True},
    ]
)
