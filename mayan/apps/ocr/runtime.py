from __future__ import unicode_literals

from django.utils.module_loading import import_string

from .settings import setting_ocr_backend, setting_ocr_backend_arguments

ocr_backend = import_string(
    dotted_path=setting_ocr_backend.value
)(**setting_ocr_backend_arguments.value)
