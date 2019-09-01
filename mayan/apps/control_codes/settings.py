from __future__ import unicode_literals

import os

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import Namespace

from .literals import DEFAULT_CONTROL_SHEET_CODE_IMAGE_CACHE_MAXIMUM_SIZE
from .utils import callback_update_control_sheet_image_cache_size

namespace = Namespace(label=_('Control codes'), name='control_codes')

setting_control_sheet_code_image_cache_maximum_size = namespace.add_setting(
    global_name='CONTROL_SHEET_CODE_IMAGE_CACHE_MAXIMUM_SIZE',
    default=DEFAULT_CONTROL_SHEET_CODE_IMAGE_CACHE_MAXIMUM_SIZE,
    help_text=_(
        'The threshold at which the CONTROL_SHEET_CODE_IMAGE_CACHE_STORAGE_BACKEND '
        'will start deleting the oldest control sheet code image cache files. '
        'Specify the size in bytes.'
    ), post_edit_function=callback_update_control_sheet_image_cache_size
)
settings_control_sheet_code_image_cache_time = namespace.add_setting(
    global_name='CONTROL_SHEETS_CODE_IMAGE_CACHE_TIME', default='31556926',
    help_text=_(
        'Time in seconds that the browser should cache the supplied control sheet '
        'code images. The default of 31559626 seconds corresponde to 1 year.'
    )
)
setting_control_sheet_code_image_cache_storage_dotted_path = namespace.add_setting(
    global_name='CONTROL_SHEETS_CODE_IMAGE_CACHE_STORAGE_BACKEND',
    default='django.core.files.storage.FileSystemStorage', help_text=_(
        'Path to the Storage subclass to use when storing the cached '
        'control sheet code image files.'
    )
)
setting_control_sheet_code_image_cache_storage_arguments = namespace.add_setting(
    global_name='CONTROL_SHEETS_CODE_IMAGE_CACHE_STORAGE_BACKEND_ARGUMENTS',
    default={'location': os.path.join(settings.MEDIA_ROOT, 'control_sheets')},
    help_text=_(
        'Arguments to pass to the CONTROL_SHEETS_CODE_IMAGE_CACHE_STORAGE_BACKEND.'
    )
)
