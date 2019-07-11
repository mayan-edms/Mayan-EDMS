from __future__ import unicode_literals

from mayan.apps.storage.utils import get_storage_subclass

from .settings import (
    setting_shared_storage, setting_shared_storage_arguments
)

storage_sharedupload = get_storage_subclass(
    dotted_path=setting_shared_storage.value
)(**setting_shared_storage_arguments.value)
