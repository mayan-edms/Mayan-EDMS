from ..classes import NamespaceMigration


class TestNamespaceMigrationOne(NamespaceMigration):
    def smart_settings_test_setting_0001(self, value):
        return '{}_0001'.format(value)


class TestNamespaceMigrationTwo(NamespaceMigration):
    def smart_settings_test_setting_0001(self, value):
        return '{}_0001'.format(value)

    def smart_settings_test_setting_0002(self, value):
        return '{}_0002'.format(value)


class TestNamespaceMigrationInvalid(NamespaceMigration):
    def smart_settings_test_setting(self, value):
        return 'invalid migration'


class TestNamespaceMigrationInvalidDual(NamespaceMigration):
    def smart_settings_test_setting_with_longer_name(self, value):
        return 'invalid migration'
