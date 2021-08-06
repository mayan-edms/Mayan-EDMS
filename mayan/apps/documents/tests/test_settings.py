from mayan.apps.documents import storages
from mayan.apps.smart_settings.tests.mixins import SmartSettingTestMixin
from mayan.apps.storage.tests.mixins import StorageSettingTestMixin
from mayan.apps.testing.tests.base import BaseTestCase

from ..literals import (
    STORAGE_NAME_DOCUMENT_FILE_PAGE_IMAGE_CACHE, STORAGE_NAME_DOCUMENT_FILES,
    STORAGE_NAME_DOCUMENT_VERSION_PAGE_IMAGE_CACHE
)
from ..settings import (
    setting_document_file_page_image_cache_storage_backend_arguments,
    setting_document_file_page_image_cache_maximum_size,
    setting_document_file_storage_backend_arguments,
    setting_document_version_page_image_cache_maximum_size,
    setting_document_version_page_image_cache_storage_backend_arguments,
    setting_language_codes
)


class DocumentSettingsTestCase(SmartSettingTestMixin, BaseTestCase):
    def test_documents_language_codes_setting_double_quotes(self):
        self._set_environment_variable(
            name='MAYAN_{}'.format(setting_language_codes.global_name),
            value='["spa","fra"]'
        )

        self.assertEqual(
            setting_language_codes.value,
            ['spa', 'fra']
        )

    def test_documents_language_codes_setting_single_quotes(self):
        self._set_environment_variable(
            name='MAYAN_{}'.format(setting_language_codes.global_name),
            value="['spa','deu']"
        )

        self.assertEqual(
            setting_language_codes.value,
            ['spa', 'deu']
        )


class DocumentFileStorageSettingsTestCase(
    SmartSettingTestMixin, StorageSettingTestMixin, BaseTestCase
):
    def test_setting_document_file_storage_backend_arguments_invalid_value(self):
        assertion = self._test_storage_setting_with_invalid_value(
            setting=setting_document_file_storage_backend_arguments,
            storage_module=storages,
            storage_name=STORAGE_NAME_DOCUMENT_FILES
        )

        self.assertTrue('Unable to initialize' in str(assertion.exception))
        self.assertTrue('document file storage' in str(assertion.exception))

    def test_setting_document_file_page_image_cache_maximum_size(self):
        old_value = setting_document_file_page_image_cache_maximum_size.value
        new_value = old_value + 1
        setting_document_file_page_image_cache_maximum_size.value = '{}'.format(new_value)

        self.assertEqual(
            setting_document_file_page_image_cache_maximum_size.value,
            new_value
        )

    def test_setting_document_file_page_image_cache_storage_backend_arguments_invalid_value(self):
        assertion = self._test_storage_setting_with_invalid_value(
            setting=setting_document_file_page_image_cache_storage_backend_arguments,
            storage_module=storages,
            storage_name=STORAGE_NAME_DOCUMENT_FILE_PAGE_IMAGE_CACHE
        )

        self.assertTrue('Unable to initialize' in str(assertion.exception))
        self.assertTrue(
            'document file image storage' in str(assertion.exception)
        )


class DocumentVersionStorageSettingsTestCase(
    SmartSettingTestMixin, StorageSettingTestMixin, BaseTestCase
):
    def test_setting_document_version_page_image_cache_storage_backend_arguments_invalid_value(self):
        assertion = self._test_storage_setting_with_invalid_value(
            setting=setting_document_version_page_image_cache_storage_backend_arguments,
            storage_module=storages,
            storage_name=STORAGE_NAME_DOCUMENT_VERSION_PAGE_IMAGE_CACHE
        )

        self.assertTrue('Unable to initialize' in str(assertion.exception))
        self.assertTrue(
            'document version image storage' in str(assertion.exception)
        )

    def test_setting_document_version_page_image_cache_maximum_size_callback(self):
        old_value = setting_document_version_page_image_cache_maximum_size.value
        new_value = old_value + 1
        setting_document_version_page_image_cache_maximum_size.value = '{}'.format(new_value)

        self.assertEqual(
            setting_document_version_page_image_cache_maximum_size.value,
            new_value
        )
