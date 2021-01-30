from django.utils.translation import ugettext_lazy as _

from mayan.apps.storage.classes import DefinedStorage

from .literals import (
    STORAGE_NAME_DOCUMENT_FILES, STORAGE_NAME_DOCUMENT_FILE_PAGE_IMAGE_CACHE,
    STORAGE_NAME_DOCUMENT_VERSION_PAGE_IMAGE_CACHE
)
from .settings import (
    setting_document_file_storage_backend,
    setting_document_file_storage_backend_arguments,
    setting_document_file_page_image_cache_storage_backend,
    setting_document_file_page_image_cache_storage_backend_arguments,
    setting_document_version_page_image_cache_storage_backend,
    setting_document_version_page_image_cache_storage_backend_arguments
)

storage_document_files = DefinedStorage(
    dotted_path=setting_document_file_storage_backend.value,
    error_message=_(
        'Unable to initialize the document file storage. Check '
        'the settings {} and {} for formatting errors.'.format(
            setting_document_file_storage_backend.global_name,
            setting_document_file_storage_backend_arguments.global_name
        )
    ),
    label=_('Document files'),
    name=STORAGE_NAME_DOCUMENT_FILES,
    kwargs=setting_document_file_storage_backend_arguments.value
)

storage_document_file_image_cache = DefinedStorage(
    dotted_path=setting_document_file_page_image_cache_storage_backend.value,
    error_message=_(
        'Unable to initialize the document file image storage. Check '
        'the settings {} and {} for formatting errors.'.format(
            setting_document_file_page_image_cache_storage_backend.global_name,
            setting_document_file_page_image_cache_storage_backend_arguments.global_name
        )
    ),
    label=_('Document file page images'),
    name=STORAGE_NAME_DOCUMENT_FILE_PAGE_IMAGE_CACHE,
    kwargs=setting_document_file_page_image_cache_storage_backend_arguments.value
)

storage_document_version_image_cache = DefinedStorage(
    dotted_path=setting_document_version_page_image_cache_storage_backend.value,
    error_message=_(
        'Unable to initialize the document version image storage. Check '
        'the settings {} and {} for formatting errors.'.format(
            setting_document_version_page_image_cache_storage_backend.global_name,
            setting_document_version_page_image_cache_storage_backend_arguments.global_name
        )
    ),
    label=_('Document version page images'),
    name=STORAGE_NAME_DOCUMENT_VERSION_PAGE_IMAGE_CACHE,
    kwargs=setting_document_version_page_image_cache_storage_backend_arguments.value
)
