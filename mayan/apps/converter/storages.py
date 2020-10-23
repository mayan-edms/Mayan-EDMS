from django.utils.translation import ugettext_lazy as _

from mayan.apps.storage.classes import DefinedStorage

from .literals import STORAGE_NAME_ASSETS
from .settings import (
    setting_storage_backend, setting_storage_backend_arguments
)

storage_assets = DefinedStorage(
    dotted_path=setting_storage_backend.value,
    error_message=_(
        'Unable to initialize the converter asset '
        'storage. Check the settings {} and {} for formatting '
        'errors.'.format(
            setting_storage_backend.global_name,
            setting_storage_backend_arguments.global_name
        )
    ), label=_('Assets'), name=STORAGE_NAME_ASSETS,
    kwargs=setting_storage_backend_arguments.value
)
