

from django.utils.translation import ugettext_lazy as _

from mayan.apps.storage.classes import DefinedStorage

from .literals import STORAGE_NAME_SOURCE_STAGING_FOLDER_FILE
from .settings import (
    setting_staging_file_image_cache_storage,
    setting_staging_file_image_cache_storage_arguments,
)

storage_staging_folder_files = DefinedStorage(
    dotted_path=setting_staging_file_image_cache_storage.value,
    error_message=_(
        'Unable to initialize the staging folder file image '
        'storage. Check the settings {} and {} for formatting '
        'errors.'.format(
            setting_staging_file_image_cache_storage.global_name,
            setting_staging_file_image_cache_storage_arguments.global_name
        )
    ),
    label=_('Staging folder files'),
    name=STORAGE_NAME_SOURCE_STAGING_FOLDER_FILE,
    kwargs=setting_staging_file_image_cache_storage_arguments.value
)
