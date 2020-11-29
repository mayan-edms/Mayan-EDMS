from django.test import override_settings

from mayan.apps.smart_settings.classes import Setting
from mayan.apps.smart_settings.tests.mixins import SmartSettingTestMixin
from mayan.apps.testing.tests.base import BaseTestCase

from ..settings import (
    setting_document_file_page_image_cache_storage_arguments,
    setting_document_file_storage_backend_arguments,
    setting_recently_accessed_document_count,
    setting_recently_created_document_count
)

from .literals import (
    TEST_DOCUMENTS_RECENTLY_ACCESSED_COUNT,
    TEST_DOCUMENTS_RECENTLY_CREATED_COUNT
)


class DocumentSettingMigrationTestCase(SmartSettingTestMixin, BaseTestCase):
    def test_documents_storage_backend_arguments_0001(self):
        test_value = {'location': 'test value'}
        self.test_setting = setting_document_file_page_image_cache_storage_arguments
        self.test_config_value = '{}'.format(
            Setting.serialize_value(value=test_value)
        )
        self._create_test_config_file()

        self.assertEqual(
            setting_document_file_page_image_cache_storage_arguments.value,
            test_value
        )

    def test_documents_storage_backend_arguments_0001_with_dict(self):
        test_value = {'location': 'test value'}
        self.test_setting = setting_document_file_page_image_cache_storage_arguments
        self.test_config_value = test_value
        self._create_test_config_file()

        self.assertEqual(
            setting_document_file_page_image_cache_storage_arguments.value,
            test_value
        )

    def test_documents_cache_storage_backend_arguments_0001(self):
        test_value = {'location': 'test value'}
        self.test_setting = setting_document_file_storage_backend_arguments
        self.test_config_value = '{}'.format(
            Setting.serialize_value(value=test_value)
        )
        self._create_test_config_file()

        self.assertEqual(
            setting_document_file_storage_backend_arguments.value,
            test_value
        )

    def test_documents_cache_storage_backend_arguments_0001_with_dict(self):
        test_value = {'location': 'test value'}
        self.test_setting = setting_document_file_storage_backend_arguments
        self.test_config_value = test_value
        self._create_test_config_file()

        self.assertEqual(
            setting_document_file_storage_backend_arguments.value,
            test_value
        )

    @override_settings(DOCUMENTS_RECENT_ACCESS_COUNT=TEST_DOCUMENTS_RECENTLY_ACCESSED_COUNT)
    def test_setting_recently_accessed_document_count_0002(self):
        test_value = None
        self.test_setting = setting_recently_accessed_document_count
        self.test_config_value = test_value
        self._create_test_config_file()

        self.assertEqual(
            setting_recently_accessed_document_count.value,
            TEST_DOCUMENTS_RECENTLY_ACCESSED_COUNT
        )

    @override_settings(DOCUMENTS_RECENT_ADDED_COUNT=TEST_DOCUMENTS_RECENTLY_CREATED_COUNT)
    def test_setting_recently_created_document_count_0002(self):
        test_value = None
        self.test_setting = setting_recently_created_document_count
        self.test_config_value = test_value
        self._create_test_config_file()

        self.assertEqual(
            setting_recently_created_document_count.value,
            TEST_DOCUMENTS_RECENTLY_CREATED_COUNT
        )
