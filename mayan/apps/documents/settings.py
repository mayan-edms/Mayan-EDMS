from __future__ import unicode_literals

import os
import pycountry

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from smart_settings.api import register_settings

LANGUAGE_CHOICES = [(i.bibliographic, _(i.name)) for i in list(pycountry.languages)]

register_settings(
    namespace='documents',
    module='documents.settings',
    settings=[
        # Storage
        {'name': 'STORAGE_BACKEND', 'global_name': 'DOCUMENTS_STORAGE_BACKEND', 'default': 'storage.backends.filebasedstorage.FileBasedStorage'},
        # Usage
        {'name': 'PREVIEW_SIZE', 'global_name': 'DOCUMENTS_PREVIEW_SIZE', 'default': '640x480'},
        {'name': 'PRINT_SIZE', 'global_name': 'DOCUMENTS_PRINT_SIZE', 'default': '1400'},
        {'name': 'MULTIPAGE_PREVIEW_SIZE', 'global_name': 'DOCUMENTS_MULTIPAGE_PREVIEW_SIZE', 'default': '160x120'},
        {'name': 'THUMBNAIL_SIZE', 'global_name': 'DOCUMENTS_THUMBNAIL_SIZE', 'default': '50x50'},
        {'name': 'DISPLAY_SIZE', 'global_name': 'DOCUMENTS_DISPLAY_SIZE', 'default': '1200'},
        {'name': 'RECENT_COUNT', 'global_name': 'DOCUMENTS_RECENT_COUNT', 'default': 40, 'description': _('Maximum number of recent (created, edited, viewed) documents to remember per user.')},
        {'name': 'ZOOM_PERCENT_STEP', 'global_name': 'DOCUMENTS_ZOOM_PERCENT_STEP', 'default': 50, 'description': _('Amount in percent zoom in or out a document page per user interaction.')},
        {'name': 'ZOOM_MAX_LEVEL', 'global_name': 'DOCUMENTS_ZOOM_MAX_LEVEL', 'default': 200, 'description': _('Maximum amount in percent (%) to allow user to zoom in a document page interactively.')},
        {'name': 'ZOOM_MIN_LEVEL', 'global_name': 'DOCUMENTS_ZOOM_MIN_LEVEL', 'default': 50, 'description': _('Minimum amount in percent (%) to allow user to zoom out a document page interactively.')},
        {'name': 'ROTATION_STEP', 'global_name': 'DOCUMENTS_ROTATION_STEP', 'default': 90, 'description': _('Amount in degrees to rotate a document page per user interaction.')},
        #
        {'name': 'CACHE_PATH', 'global_name': 'DOCUMENTS_CACHE_PATH', 'default': os.path.join(settings.MEDIA_ROOT, 'image_cache'), 'exists': True},
        {'name': 'LANGUAGE', 'global_name': 'DOCUMENTS_LANGUAGE', 'default': 'eng', 'description': _('Default documents language (in ISO639-2 format).')},
        {'name': 'LANGUAGE_CHOICES', 'global_name': 'DOCUMENTS_LANGUAGE_CHOICES', 'default': LANGUAGE_CHOICES, 'description': _('List of supported document languages.')},
    ]
)
