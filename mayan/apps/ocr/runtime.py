from __future__ import unicode_literals

import yaml

try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader

from django.utils.module_loading import import_string

from .settings import setting_ocr_backend, setting_ocr_backend_arguments

ocr_backend = import_string(
    dotted_path=setting_ocr_backend.value
)(
    **yaml.load(
        stream=setting_ocr_backend_arguments.value or '{}', Loader=SafeLoader
    )
)
