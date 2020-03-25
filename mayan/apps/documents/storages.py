from django.utils.translation import ugettext_lazy as _

from mayan.apps.storage.classes import DefinedStorage

from .literals import (
    STORAGE_NAME_DOCUMENT_IMAGE, STORAGE_NAME_DOCUMENT_VERSION
)
from .settings import (
    setting_documentimagecache_storage,
    setting_documentimagecache_storage_arguments,
    setting_storage_backend, setting_storage_backend_arguments
)

storage_document_image_cache = DefinedStorage(
    dotted_path=setting_documentimagecache_storage.value,
    error_message=_(
        'Unable to initialize the document image storage. Check '
        'the settings {} and {} for formatting errors.'.format(
            setting_documentimagecache_storage.global_name,
            setting_documentimagecache_storage_arguments.global_name
        )
    ),
    label=_('Document images'),
    name=STORAGE_NAME_DOCUMENT_IMAGE,
    kwargs=setting_documentimagecache_storage_arguments.value
)

storage_document_versions = DefinedStorage(
    dotted_path=setting_storage_backend.value,
    error_message=_(
        'Unable to initialize the document version storage. Check '
        'the settings {} and {} for formatting errors.'.format(
            setting_storage_backend.global_name,
            setting_storage_backend_arguments.global_name
        )
    ),
    label=_('Document version files'),
    name=STORAGE_NAME_DOCUMENT_VERSION,
    kwargs=setting_storage_backend_arguments.value
)
