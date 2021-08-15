from django.test import override_settings

from mayan.apps.smart_settings.tests.mixins import SmartSettingTestMixin
from mayan.apps.testing.tests.base import BaseTestCase

from ..literals import DEFAULT_SOURCES_CACHE_STORAGE_BACKEND
from ..settings import (
    setting_source_cache_storage_backend,
    setting_source_cache_storage_backend_arguments
)

from .literals import (
    TEST_SOURCES_STAGING_FILE_CACHE_STORAGE_BACKEND,
    TEST_SOURCES_STAGING_FILE_CACHE_STORAGE_BACKEND_ARGUMENTS
)


class SourceSettingMigrationTestCase(SmartSettingTestMixin, BaseTestCase):
    @override_settings(
        SOURCES_STAGING_FILE_CACHE_STORAGE_BACKEND=TEST_SOURCES_STAGING_FILE_CACHE_STORAGE_BACKEND
    )
    def test_setting_source_cache_storage_backend_0002(self):
        test_value = None
        self.test_setting = setting_source_cache_storage_backend
        self.test_config_value = test_value
        self._create_test_config_file()

        self.assertEqual(
            setting_source_cache_storage_backend.value,
            TEST_SOURCES_STAGING_FILE_CACHE_STORAGE_BACKEND
        )

    @override_settings(
        SOURCES_STAGING_FILE_CACHE_STORAGE_BACKEND_ARGUMENTS=TEST_SOURCES_STAGING_FILE_CACHE_STORAGE_BACKEND_ARGUMENTS
    )
    def test_setting_source_cache_storage_backend_arguments_0002(self):
        test_value = None
        self.test_setting = setting_source_cache_storage_backend_arguments
        self.test_config_value = test_value
        self._create_test_config_file()

        self.assertEqual(
            setting_source_cache_storage_backend_arguments.value,
            TEST_SOURCES_STAGING_FILE_CACHE_STORAGE_BACKEND_ARGUMENTS
        )

    def test_setting_source_cache_storage_backend_0002_no_value(self):
        test_value = None
        self.test_setting = setting_source_cache_storage_backend
        self.test_config_value = test_value
        self._create_test_config_file()

        self.assertEqual(
            setting_source_cache_storage_backend.value,
            DEFAULT_SOURCES_CACHE_STORAGE_BACKEND
        )
