from django.utils.translation import ugettext_lazy as _

from .classes import DefinedStorage
from .literals import STORAGE_NAME_SHARED_UPLOADED_FILE
from .settings import (
    setting_shared_storage, setting_shared_storage_arguments
)

storage_shared_uploaded_files = DefinedStorage(
    dotted_path=setting_shared_storage.value,
    error_message=_(
        'Unable to initialize the shared uploaded file '
        'storage. Check the settings {} and {} for formatting '
        'errors.'.format(
            setting_shared_storage.global_name,
            setting_shared_storage_arguments.global_name
        )
    ),
    label=_('Shared uploaded files'),
    name=STORAGE_NAME_SHARED_UPLOADED_FILE,
    kwargs=setting_shared_storage_arguments.value
)
