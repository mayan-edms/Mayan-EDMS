from mayan.apps.common.tests.base import BaseTestCase
from mayan.apps.smart_settings.classes import Setting
from mayan.apps.smart_settings.tests.mixins import SmartSettingTestMixin

from ..settings import setting_graphics_backend_arguments


class ConverterSettingMigrationTestCase(
    SmartSettingTestMixin, BaseTestCase
):
    def test_converter_graphics_backend_arguments_0001_migration(self):
        test_value = {'location': 'test value'}
        self.test_setting = setting_graphics_backend_arguments
        self.test_config_value = '{}'.format(
            Setting.serialize_value(value=test_value)
        )
        self._create_test_config_file()

        self.assertEqual(
            setting_graphics_backend_arguments.value,
            test_value
        )

    def test_converter_graphics_backend_arguments_0001_migration_with_dict(self):
        test_value = {'location': 'test value'}
        self.test_setting = setting_graphics_backend_arguments
        self.test_config_value = test_value
        self._create_test_config_file()

        self.assertEqual(
            setting_graphics_backend_arguments.value,
            test_value
        )
