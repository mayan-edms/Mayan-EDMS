from __future__ import unicode_literals

from django.utils.module_loading import import_string

from .settings import setting_graphics_backend

backend = converter_class = import_string(
    dotted_path=setting_graphics_backend.value
)
