from mayan.apps.smart_settings.classes import Setting
from mayan.apps.smart_settings.tests.mixins import SmartSettingTestMixin
from mayan.apps.testing.tests.base import BaseTestCase

from ..settings import setting_drivers_arguments


class FileMetadataSettingMigrationTestCase(
    SmartSettingTestMixin, BaseTestCase
):
    def test_file_metadata_drivers_arguments_0001_migration(self):
        test_value = {'location': 'test value'}
        self.test_setting = setting_drivers_arguments
        self.test_config_value = '{}'.format(
            Setting.serialize_value(value=test_value)
        )
        self._create_test_config_file()

        self.assertEqual(
            setting_drivers_arguments.value,
            test_value
        )

    def test_file_metadata_drivers_arguments_0001_migration_with_dict(self):
        test_value = {'location': 'test value'}
        self.test_setting = setting_drivers_arguments
        self.test_config_value = test_value
        self._create_test_config_file()

        self.assertEqual(
            setting_drivers_arguments.value,
            test_value
        )
