from mayan.apps.smart_settings.classes import SettingNamespaceMigration, Setting
from mayan.apps.smart_settings.utils import smart_yaml_load


class DocumentsSettingMigration(SettingNamespaceMigration):
    """
    0001 to 0002: backend arguments are no longer quoted but YAML valid
                  too. Changed in version 3.3.
    0002 to 0003: Setting DOCUMENTS_RECENT_ADDED_COUNT renamed to
                  DOCUMENTS_RECENTLY_CREATED_COUNT,
                  DOCUMENTS_RECENT_ADDED_COUNT renamed to
                  DOCUMENTS_RECENTLY_CREATED_COUNT. Changed in version 4.0.
    """
    def documents_cache_storage_backend_arguments_0001(self, value):
        return smart_yaml_load(value=value)

    def documents_storage_backend_arguments_0001(self, value):
        return smart_yaml_load(value=value)

    def documents_recently_accessed_count_0002(self, value):
        # Get the setting by its new global name
        setting = Setting.get(global_name='DOCUMENTS_RECENTLY_ACCESSED_COUNT')
        # Load the value from the setting's old global name
        setting.cache_value(global_name='DOCUMENTS_RECENT_ACCESS_COUNT')
        return setting.value

    def documents_recently_created_count_0002(self, value):
        # Get the setting by its new global name
        setting = Setting.get(global_name='DOCUMENTS_RECENTLY_CREATED_COUNT')
        # Load the value from the setting's old global name
        setting.cache_value(global_name='DOCUMENTS_RECENT_ADDED_COUNT')
        return setting.value
