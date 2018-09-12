from __future__ import unicode_literals

import yaml

from django.utils.module_loading import import_string

from .settings import (
    setting_staging_file_image_cache_storage,
    setting_staging_file_image_cache_storage_arguments,
)

storage_staging_file_image_cache = import_string(
    dotted_path=setting_staging_file_image_cache_storage.value
)(
    **yaml.safe_load(
        setting_staging_file_image_cache_storage_arguments.value or '{}'
    )
)
