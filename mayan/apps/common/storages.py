from __future__ import unicode_literals

import yaml

from django.utils.module_loading import import_string

from .settings import (
    setting_shared_storage, setting_shared_storage_arguments
)

storage_sharedupload = import_string(
    dotted_path=setting_shared_storage.value
)(
    **yaml.safe_load(
        setting_shared_storage_arguments.value or '{}'
    )
)
