from __future__ import unicode_literals

import yaml

try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader

from django.utils.module_loading import import_string

from .settings import (
    setting_shared_storage, setting_shared_storage_arguments
)

storage_sharedupload = import_string(
    dotted_path=setting_shared_storage.value
)(
    **yaml.load(
        stream=setting_shared_storage_arguments.value or '{}',
        Loader=SafeLoader
    )
)
