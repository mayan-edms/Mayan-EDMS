from django.utils.module_loading import import_string

from .settings import BACKEND

ocr_backend_class = import_string(BACKEND)
