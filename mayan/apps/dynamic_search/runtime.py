from django.utils.module_loading import import_string

from .settings import (
    setting_search_backend, setting_search_backend_arguments
)

search_backend = import_string(dotted_path=setting_search_backend.value)(
    **setting_search_backend_arguments.value
)
