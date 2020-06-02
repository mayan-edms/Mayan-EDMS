from pathlib import Path

from django.conf import settings
from django.utils.encoding import force_text

from mayan.apps.common.settings import setting_paginate_by
from mayan.apps.tests.tests.base import BaseTestCase
from mayan.apps.storage.utils import fs_cleanup

from ..classes import Setting

from .literals import (
    ENVIRONMENT_TEST_NAME, ENVIRONMENT_TEST_VALUE, TEST_SETTING_GLOBAL_NAME,
    TEST_SETTING_INITIAL_VALUE, TEST_SETTING_VALUE
)
from .mixins import SmartSettingTestMixin
from .mocks import (
    TestNamespaceMigrationOne, TestNamespaceMigrationTwo,
    TestNamespaceMigrationInvalid, TestNamespaceMigrationInvalidDual
)


class ClassesTestCase(SmartSettingTestMixin, BaseTestCase):
    def test_environment_override(self):
        test_environment_value = 'test environment value'
        test_file_value = 'test file value'

        self._create_test_settings_namespace()
        self._create_test_setting()

        self._set_environment_variable(
            name='MAYAN_{}'.format(self.test_setting.global_name),
            value=test_environment_value
        )

        self.test_config_value = test_file_value
        self._create_test_config_file()

        self.assertEqual(
            self.test_setting.value, test_environment_value
        )

    def test_environment_variable(self):
        self._set_environment_variable(
            name='MAYAN_{}'.format(ENVIRONMENT_TEST_NAME),
            value=ENVIRONMENT_TEST_VALUE
        )

        self.assertTrue(setting_paginate_by.value, ENVIRONMENT_TEST_VALUE)

    def test_config_backup_creation(self):
        path_config_backup = Path(settings.CONFIGURATION_LAST_GOOD_FILEPATH)
        fs_cleanup(filename=force_text(path_config_backup))

        Setting.save_last_known_good()
        self.assertTrue(path_config_backup.exists())

    def test_config_backup_creation_no_tags(self):
        path_config_backup = Path(settings.CONFIGURATION_LAST_GOOD_FILEPATH)
        fs_cleanup(filename=force_text(path_config_backup))

        Setting.save_last_known_good()
        self.assertTrue(path_config_backup.exists())

        with path_config_backup.open(mode='r') as file_object:
            self.assertFalse('!!python/' in file_object.read())

    def test_setting_check_changed(self):
        self._create_test_settings_namespace()
        test_setting = self.test_settings_namespace.add_setting(
            global_name='SMART_SETTINGS_TEST_SETTING',
            default='test value'
        )
        # Initialize hash cache
        Setting._cache_hash = None
        Setting.check_changed()
        self.assertFalse(Setting.check_changed())
        test_setting.value = 'test value edited'
        self.assertTrue(Setting.check_changed())


class SettingNamespaceMigrationTestCase(SmartSettingTestMixin, BaseTestCase):
    def test_environment_migration(self):
        self._set_environment_variable(
            name='MAYAN_{}'.format(TEST_SETTING_GLOBAL_NAME),
            value=TEST_SETTING_INITIAL_VALUE
        )
        self._create_test_settings_namespace(
            migration_class=TestNamespaceMigrationOne, version='0002'
        )
        self._create_test_setting()

        self.assertEqual(
            self.test_setting.value, TEST_SETTING_INITIAL_VALUE
        )

    def test_migration_0001_to_0002(self):
        self._create_test_settings_namespace(
            migration_class=TestNamespaceMigrationTwo, version='0002'
        )
        self._create_test_setting()

        self.test_config_value = TEST_SETTING_VALUE
        self._create_test_config_file()

        self.assertEqual(
            self.test_setting.value, '{}_0001'.format(TEST_SETTING_VALUE)
        )

    def test_migration_0001_to_0003(self):
        self._create_test_settings_namespace(
            migration_class=TestNamespaceMigrationTwo, version='0003'
        )
        self._create_test_setting()

        self.test_config_value = TEST_SETTING_VALUE
        self._create_test_config_file()

        self.assertEqual(
            self.test_setting.value, '{}_0001_0002'.format(TEST_SETTING_VALUE)
        )

    def test_migration_invalid(self):
        self._create_test_settings_namespace(
            migration_class=TestNamespaceMigrationInvalid, version='0002'
        )
        self._create_test_setting()

        self.test_config_value = TEST_SETTING_VALUE
        self._create_test_config_file()

        self.assertEqual(
            self.test_setting.value, TEST_SETTING_VALUE
        )

    def test_migration_invalid_dual(self):
        self._create_test_settings_namespace(
            migration_class=TestNamespaceMigrationInvalidDual, version='0002'
        )
        self._create_test_setting()

        self.test_config_value = TEST_SETTING_VALUE
        self._create_test_config_file()

        self.assertEqual(
            self.test_setting.value, TEST_SETTING_VALUE
        )
