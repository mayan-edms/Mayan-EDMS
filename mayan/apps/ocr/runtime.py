from django.utils.module_loading import import_string

from .settings import BACKEND

ocr_backend = import_string(BACKEND)()
