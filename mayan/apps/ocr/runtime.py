from __future__ import unicode_literals

import yaml

from django.utils.module_loading import import_string

from .settings import setting_ocr_backend, setting_ocr_backend_arguments

ocr_backend = import_string(
    setting_ocr_backend.value
)(
    **yaml.safe_load(
        setting_ocr_backend_arguments.value or '{}'
    )
)
