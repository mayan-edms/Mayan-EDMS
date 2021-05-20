from mayan.apps.smart_settings.classes import SettingNamespaceMigration, Setting
from mayan.apps.smart_settings.utils import smart_yaml_load

from .literals import (
    DEFAULT_DOCUMENTS_STORAGE_BACKEND,
    DEFAULT_DOCUMENTS_STORAGE_BACKEND_ARGUMENTS
)


class DocumentsSettingMigration(SettingNamespaceMigration):
    """
    0001 to 0002: Backend arguments are no longer quoted but YAML valid
                  too. Changed in version 3.3.
    0002 to 0003: Setting DOCUMENTS_RECENT_ADDED_COUNT renamed to
                  DOCUMENTS_RECENTLY_CREATED_COUNT,
                  DOCUMENTS_RECENT_ADDED_COUNT renamed to
                  DOCUMENTS_RECENTLY_CREATED_COUNT. Changed in version 4.0.
    0003 to 0004: New settings for document file storage, file page image
                  cache and version page image cache added and made to take
                  their initial settings from existing
                  DOCUMENTS_CACHE_STORAGE_BACKEND,
                  DOCUMENTS_CACHE_STORAGE_BACKEND_ARGUMENTS,
                  DOCUMENTS_STORAGE_BACKEND, and
                  DOCUMENTS_STORAGE_BACKEND_ARGUMENTS settings.
    """
    def documents_cache_storage_backend_arguments_0001(self, value):
        return smart_yaml_load(value=value)

    def documents_storage_backend_arguments_0001(self, value):
        return smart_yaml_load(value=value)

    def documents_file_page_image_cache_storage_backend_0003(self, value):
        # Get the setting by its new global name
        setting = Setting.get(
            global_name='DOCUMENTS_FILE_PAGE_IMAGE_CACHE_STORAGE_BACKEND'
        )
        # Load the value from the setting's old global name
        setting.cache_value(global_name='DOCUMENTS_CACHE_STORAGE_BACKEND')
        return setting.value

    def documents_file_page_image_cache_storage_backend_arguments_0003(self, value):
        # Get the setting by its new global name
        setting = Setting.get(
            global_name='DOCUMENTS_FILE_PAGE_IMAGE_CACHE_STORAGE_BACKEND_ARGUMENTS'
        )
        # Load the value from the setting's old global name
        setting.cache_value(
            global_name='DOCUMENTS_CACHE_STORAGE_BACKEND_ARGUMENTS'
        )
        return setting.value

    def documents_file_storage_backend_0003(self, value):
        # Get the setting by its new global name
        setting = Setting.get(global_name='DOCUMENTS_FILE_STORAGE_BACKEND')
        # Load the value from the setting's old global name
        setting.cache_value(
            global_name='DOCUMENTS_STORAGE_BACKEND',
            default_override=DEFAULT_DOCUMENTS_STORAGE_BACKEND
        )
        return setting.value

    def documents_file_storage_backend_arguments_0003(self, value):
        # Get the setting by its new global name
        setting = Setting.get(
            global_name='DOCUMENTS_FILE_STORAGE_BACKEND_ARGUMENTS'
        )
        # Load the value from the setting's old global name
        setting.cache_value(
            global_name='DOCUMENTS_STORAGE_BACKEND_ARGUMENTS',
            default_override=DEFAULT_DOCUMENTS_STORAGE_BACKEND_ARGUMENTS
        )
        return setting.value

    def documents_recently_accessed_count_0002(self, value):
        # Get the setting by its new global name
        setting = Setting.get(
            global_name='DOCUMENTS_RECENTLY_ACCESSED_COUNT'
        )
        # Load the value from the setting's old global name
        setting.cache_value(global_name='DOCUMENTS_RECENT_ACCESS_COUNT')
        return setting.value

    def documents_recently_created_count_0002(self, value):
        # Get the setting by its new global name
        setting = Setting.get(global_name='DOCUMENTS_RECENTLY_CREATED_COUNT')
        # Load the value from the setting's old global name
        setting.cache_value(global_name='DOCUMENTS_RECENT_ADDED_COUNT')
        return setting.value

    def documents_version_page_image_cache_storage_backend_0003(self, value):
        # Get the setting by its new global name
        setting = Setting.get(
            global_name='DOCUMENTS_VERSION_PAGE_IMAGE_CACHE_STORAGE_BACKEND'
        )
        # Load the value from the setting's old global name
        setting.cache_value(global_name='DOCUMENTS_CACHE_STORAGE_BACKEND')
        return setting.value

    def documents_version_page_image_cache_storage_backend_arguments_0003(self, value):
        # Get the setting by its new global name
        setting = Setting.get(
            global_name='DOCUMENTS_VERSION_PAGE_IMAGE_CACHE_STORAGE_BACKEND_ARGUMENTS'
        )
        # Load the value from the setting's old global name
        setting.cache_value(
            global_name='DOCUMENTS_CACHE_STORAGE_BACKEND_ARGUMENTS'
        )
        return setting.value
