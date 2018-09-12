from __future__ import unicode_literals

import os

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from smart_settings import Namespace

namespace = Namespace(name='sources', label=_('Sources'))

setting_scanimage_path = namespace.add_setting(
    global_name='SOURCES_SCANIMAGE_PATH', default='/usr/bin/scanimage',
    help_text=_(
        'File path to the scanimage program used to control image scanners.'
    ),
    is_path=True
)
setting_staging_file_image_cache_storage = namespace.add_setting(
    global_name='SOURCES_STAGING_FILE_CACHE_STORAGE_BACKEND',
    default='django.core.files.storage.FileSystemStorage', help_text=_(
        'Path to the Storage subclass to use when storing the cached '
        'staging_file image files.'
    ), quoted=True
)
setting_staging_file_image_cache_storage_arguments = namespace.add_setting(
    global_name='SOURCES_STAGING_FILE_CACHE_STORAGE_BACKEND_ARGUMENTS',
    default='{{location: {}}}'.format(
        os.path.join(settings.MEDIA_ROOT, 'staging_file_cache')
    ), help_text=_(
        'Arguments to pass to the SOURCES_STAGING_FILE_CACHE_STORAGE_BACKEND.'
    ), quoted=True,
)
settings_staging_file_image_cache_time = namespace.add_setting(
    global_name='SOURCES_STAGING_FILE_IMAGE_CACHE_TIME', default='31556926',
    help_text=_(
        'Time in seconds that the browser should cache the supplied staging '
        'file images. The default of 31559626 seconds corresponde to 1 year.'
    )
)
