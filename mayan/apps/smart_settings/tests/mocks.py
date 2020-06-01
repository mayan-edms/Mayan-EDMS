from ..classes import SettingNamespaceMigration


class TestNamespaceMigrationOne(SettingNamespaceMigration):
    def smart_settings_test_setting_0001(self, value):
        return '{}_0001'.format(value)


class TestNamespaceMigrationTwo(SettingNamespaceMigration):
    def smart_settings_test_setting_0001(self, value):
        return '{}_0001'.format(value)

    def smart_settings_test_setting_0002(self, value):
        return '{}_0002'.format(value)


class TestNamespaceMigrationInvalid(SettingNamespaceMigration):
    def smart_settings_test_setting(self, value):
        return 'invalid migration'


class TestNamespaceMigrationInvalidDual(SettingNamespaceMigration):
    def smart_settings_test_setting_with_longer_name(self, value):
        return 'invalid migration'
