from __future__ import unicode_literals

import yaml

from django.utils.module_loading import import_string

from .settings import (
    setting_documentimagecache_storage, setting_documentimagecache_storage_arguments,
    setting_storage_backend, setting_storage_backend_arguments
)

documentversion_storage = import_string(
    dotted_path=setting_storage_backend.value
)(
    **yaml.safe_load(
        setting_storage_backend_arguments.value or '{}'
    )
)

documentimagecache_storage = import_string(
    dotted_path=setting_documentimagecache_storage.value
)(
    **yaml.safe_load(
        setting_documentimagecache_storage_arguments.value or '{}'
    )
)
