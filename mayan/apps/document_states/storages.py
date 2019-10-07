from __future__ import unicode_literals

from mayan.apps.storage.utils import get_storage_subclass

from .settings import (
    setting_workflowimagecache_storage,
    setting_workflowimagecache_storage_arguments
)

storage_workflowimagecache = get_storage_subclass(
    dotted_path=setting_workflowimagecache_storage.value
)(**setting_workflowimagecache_storage_arguments.value)
