from __future__ import unicode_literals

import logging

from django.utils.six import raise_from

from mayan.apps.storage.utils import get_storage_subclass

from .settings import (
    setting_storage_backend, setting_storage_backend_arguments
)

logger = logging.getLogger(__name__)

try:
    storage_detachedsignature = get_storage_subclass(
        dotted_path=setting_storage_backend.value
    )(**setting_storage_backend_arguments.value)
except Exception as exception:
    message = (
        'Unable to initialize the detached signature storage. Check the '
        'settings {} and {} for formatting errors.'.format(
            setting_storage_backend.global_name,
            setting_storage_backend_arguments.global_name
        )
    )

    logger.fatal(message)
    raise_from(value=TypeError(message), from_value=exception)
