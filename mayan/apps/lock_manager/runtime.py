from django.utils.module_loading import import_string

from .settings import setting_backend

locking_backend = import_string(dotted_path=setting_backend.value)
