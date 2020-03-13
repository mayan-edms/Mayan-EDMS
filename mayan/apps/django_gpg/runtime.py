from django.utils.module_loading import import_string

from .settings import setting_gpg_path

SETTING_GPG_BACKEND = 'mayan.apps.django_gpg.classes.PythonGNUPGBackend'

gpg_backend = import_string(dotted_path=SETTING_GPG_BACKEND)(
    binary_path=setting_gpg_path.value
)
