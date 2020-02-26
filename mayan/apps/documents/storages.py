from __future__ import unicode_literals

import logging

from django.utils.six import raise_from

from mayan.apps.storage.utils import get_storage_subclass

from .settings import (
    setting_documentimagecache_storage,
    setting_documentimagecache_storage_arguments,
    setting_storage_backend, setting_storage_backend_arguments
)

logger = logging.getLogger(__name__)

try:
    storage_documentversion = get_storage_subclass(
        dotted_path=setting_storage_backend.value
    )(**setting_storage_backend_arguments.value)
except Exception as exception:
    message = (
        'Unable to initialize the document version storage. Check the '
        'settings {} and {} for formatting errors.'.format(
            setting_storage_backend.global_name,
            setting_storage_backend_arguments.global_name
        )
    )

    logger.fatal(message)
    raise_from(value=TypeError(message), from_value=exception)

try:
    storage_documentimagecache = get_storage_subclass(
        dotted_path=setting_documentimagecache_storage.value
    )(**setting_documentimagecache_storage_arguments.value)
except Exception as exception:
    message = (
        'Unable to initialize the document image cache storage. '
        'Check the settings {} and {} for formatting errors.'.format(
            setting_documentimagecache_storage.global_name,
            setting_documentimagecache_storage_arguments.global_name
        )
    )

    logger.fatal(message)
    raise_from(value=TypeError(message), from_value=exception)
