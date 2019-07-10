from __future__ import unicode_literals

from django.utils.module_loading import import_string

from mayan.apps.common.serialization import yaml_load

from .settings import (
    setting_shared_storage, setting_shared_storage_arguments
)

storage_sharedupload = import_string(
    dotted_path=setting_shared_storage.value
)(
    **yaml_load(
        stream=setting_shared_storage_arguments.value or '{}',
    )
)
