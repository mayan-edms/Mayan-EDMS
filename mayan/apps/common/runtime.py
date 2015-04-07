from django.utils.module_loading import import_string

from .settings import SHARED_STORAGE

shared_storage_backend = import_string(SHARED_STORAGE)()
