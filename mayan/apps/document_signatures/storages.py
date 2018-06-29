from __future__ import unicode_literals

import yaml

from django.utils.module_loading import import_string

from .settings import (
    setting_storage_backend, setting_storage_backend_arguments
)

storage_detachedsignature = import_string(
    dotted_path=setting_storage_backend.value
)(
    **yaml.safe_load(
        setting_storage_backend_arguments.value or '{}'
    )
)
