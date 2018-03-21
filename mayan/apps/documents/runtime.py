from __future__ import unicode_literals

import yaml

from django.utils.module_loading import import_string

from .settings import (
    setting_cache_storage_backend, setting_cache_storage_backend_arguments,
    setting_storage_backend, setting_storage_backend_arguments
)

storage_backend = import_string(
    dotted_path=setting_storage_backend.value
)(
    **yaml.safe_load(
        setting_storage_backend_arguments.value or '{}'
    )
)

cache_storage_backend = import_string(
    dotted_path=setting_cache_storage_backend.value
)(
    **yaml.safe_load(
        setting_cache_storage_backend_arguments.value or '{}'
    )
)
