from __future__ import unicode_literals

from django.utils.module_loading import import_string

from .settings import (
    setting_documentimagecache_storage,
    setting_documentimagecache_storage_arguments,
    setting_storage_backend, setting_storage_backend_arguments
)

storage_documentversion = import_string(
    dotted_path=setting_storage_backend.value
)(**setting_storage_backend_arguments.value)

storage_documentimagecache = import_string(
    dotted_path=setting_documentimagecache_storage.value
)(**setting_documentimagecache_storage_arguments.value)
