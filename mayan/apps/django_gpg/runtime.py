from django.utils.module_loading import import_string

from .settings import (
    setting_gpg_backend, setting_gpg_backend_arguments
)

gpg_backend = import_string(dotted_path=setting_gpg_backend.value)(
    **setting_gpg_backend_arguments.value
)
