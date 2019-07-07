from __future__ import unicode_literals

from django.utils.module_loading import import_string

from .settings import (
    setting_workflowimagecache_storage,
    setting_workflowimagecache_storage_arguments
)

storage_workflowimagecache = import_string(
    dotted_path=setting_workflowimagecache_storage.value
)(**setting_workflowimagecache_storage_arguments.value)
