from __future__ import unicode_literals

import os

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from smart_settings import Namespace

from .literals import DEFAULT_LANGUAGE, DEFAULT_LANGUAGE_CODES

namespace = Namespace(name='documents', label=_('Documents'))
setting_display_width = namespace.add_setting(
    global_name='DOCUMENTS_DISPLAY_WIDTH', default='3600'
)
setting_display_height = namespace.add_setting(
    global_name='DOCUMENTS_DISPLAY_HEIGHT', default=''
)
setting_preview_width = namespace.add_setting(
    global_name='DOCUMENTS_PREVIEW_WIDTH', default='800'
)
setting_preview_height = namespace.add_setting(
    global_name='DOCUMENTS_PREVIEW_HEIGHT', default=''
)
setting_print_width = namespace.add_setting(
    global_name='DOCUMENTS_PRINT_WIDTH', default='3600'
)
setting_print_height = namespace.add_setting(
    global_name='DOCUMENTS_PRINT_HEIGHT', default=''
)
setting_thumbnail_width = namespace.add_setting(
    global_name='DOCUMENTS_THUMBNAIL_WIDTH', default='800'
)
setting_thumbnail_height = namespace.add_setting(
    global_name='DOCUMENTS_THUMBNAIL_HEIGHT', default=''
)
setting_recent_count = namespace.add_setting(
    global_name='DOCUMENTS_RECENT_COUNT', default=40,
    help_text=_(
        'Maximum number of recent (created, edited, viewed) documents to '
        'remember per user.'
    )
)
setting_storage_backend = namespace.add_setting(
    global_name='DOCUMENTS_STORAGE_BACKEND',
    default='django.core.files.storage.FileSystemStorage'
)
setting_storage_backend_arguments = namespace.add_setting(
    global_name='DOCUMENTS_STORAGE_BACKEND_ARGUMENTS',
    default='{{location: {}}}'.format(
        os.path.join(settings.MEDIA_ROOT, 'document_storage')
    )
)
setting_zoom_percent_step = namespace.add_setting(
    global_name='DOCUMENTS_ZOOM_PERCENT_STEP', default=25,
    help_text=_(
        'Amount in percent zoom in or out a document page per user '
        'interaction.'
    )
)
setting_zoom_max_level = namespace.add_setting(
    global_name='DOCUMENTS_ZOOM_MAX_LEVEL', default=300,
    help_text=_(
        'Maximum amount in percent (%) to allow user to zoom in a document '
        'page interactively.'
    )
)
setting_zoom_min_level = namespace.add_setting(
    global_name='DOCUMENTS_ZOOM_MIN_LEVEL', default=25,
    help_text=_(
        'Minimum amount in percent (%) to allow user to zoom out a document '
        'page interactively.'
    )
)
setting_rotation_step = namespace.add_setting(
    global_name='DOCUMENTS_ROTATION_STEP', default=90,
    help_text=_(
        'Amount in degrees to rotate a document page per user interaction.'
    )
)
setting_documentimagecache_storage = namespace.add_setting(
    global_name='DOCUMENTS_CACHE_STORAGE_BACKEND',
    default='django.core.files.storage.FileSystemStorage'
)
setting_documentimagecache_storage_arguments = namespace.add_setting(
    global_name='DOCUMENTS_CACHE_STORAGE_BACKEND_ARGUMENTS',
    default='{{location: {}}}'.format(
        os.path.join(settings.MEDIA_ROOT, 'document_cache')
    )
)
setting_language = namespace.add_setting(
    global_name='DOCUMENTS_LANGUAGE', default=DEFAULT_LANGUAGE,
    help_text=_('Default documents language (in ISO639-3 format).')
)
setting_language_codes = namespace.add_setting(
    global_name='DOCUMENTS_LANGUAGE_CODES', default=DEFAULT_LANGUAGE_CODES,
    help_text=_('List of supported document languages. In ISO639-3 format.')
)
setting_disable_base_image_cache = namespace.add_setting(
    global_name='DOCUMENTS_DISABLE_BASE_IMAGE_CACHE', default=False,
    help_text=_(
        'Disables the first cache tier which stores high resolution, '
        'non transformed versions of documents\'s pages.'
    )
)
setting_disable_transformed_image_cache = namespace.add_setting(
    global_name='DOCUMENTS_DISABLE_TRANSFORMED_IMAGE_CACHE', default=False,
    help_text=_(
        'Disables the second cache tier which stores medium to low '
        'resolution, transformed (rotated, zoomed, etc) versions '
        'of documents\' pages.'
    )
)
setting_fix_orientation = namespace.add_setting(
    global_name='DOCUMENTS_FIX_ORIENTATION', default=False,
    help_text=_(
        'Detect the orientation of each of the document\'s pages '
        'and create a corresponding rotation transformation to '
        'display it rightside up. This is an experimental '
        'feature and it is disabled by default.'
    )
)
