from __future__ import unicode_literals

from mayan.apps.storage.utils import get_storage_subclass

from .settings import (
    setting_staging_file_image_cache_storage,
    setting_staging_file_image_cache_storage_arguments,
)

storage_staging_file_image_cache = get_storage_subclass(
    dotted_path=setting_staging_file_image_cache_storage.value
)(**setting_staging_file_image_cache_storage_arguments.value)
