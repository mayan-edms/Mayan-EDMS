from django.utils.module_loading import import_string

from .settings import STORAGE_BACKEND

storage_backend = import_string(STORAGE_BACKEND)()
