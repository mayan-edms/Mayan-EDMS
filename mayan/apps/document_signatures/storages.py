from django.utils.translation import ugettext_lazy as _

from mayan.apps.storage.classes import DefinedStorage

from .literals import STORAGE_NAME_DOCUMENT_SIGNATURES_DETACHED_SIGNATURE
from .settings import (
    setting_storage_backend, setting_storage_backend_arguments
)


storage_document_signatures_detached = DefinedStorage(
    dotted_path=setting_storage_backend.value,
    error_message=_(
        'Unable to initialize the detached signatures '
        'storage. Check the settings {} and {} for formatting '
        'errors.'.format(
            setting_storage_backend.global_name,
            setting_storage_backend_arguments.global_name
        )
    ),
    label=_('Detached signatures'),
    name=STORAGE_NAME_DOCUMENT_SIGNATURES_DETACHED_SIGNATURE,
    kwargs=setting_storage_backend_arguments.value
)
