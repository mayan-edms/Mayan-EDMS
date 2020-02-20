from __future__ import unicode_literals

import logging

from django.utils.six import raise_from

from mayan.apps.storage.utils import get_storage_subclass

from .settings import (
    setting_staging_file_image_cache_storage,
    setting_staging_file_image_cache_storage_arguments,
)

logger = logging.getLogger(__name__)

try:
    storage_staging_file_image_cache = get_storage_subclass(
        dotted_path=setting_staging_file_image_cache_storage.value
    )(**setting_staging_file_image_cache_storage_arguments.value)
except Exception as exception:
    message = (
        'Unable to initialize the staging file image cache storage. Check '
        'the settings {} and {} for formatting errors.'.format(
            setting_staging_file_image_cache_storage.global_name,
            setting_staging_file_image_cache_storage_arguments.global_name
        )
    )
    logger.fatal(message)
    raise_from(value=TypeError(message), from_value=exception)
