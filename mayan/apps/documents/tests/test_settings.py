from __future__ import unicode_literals

import importlib
import logging

from mayan.apps.common.tests.base import BaseTestCase
from mayan.apps.documents import storages
from mayan.apps.documents.settings import (
    setting_documentimagecache_storage_arguments,
    setting_storage_backend_arguments
)
from mayan.apps.smart_settings.tests.mixins import SmartSettingTestMixin

from ..settings import setting_language_codes


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


class DocumentStorageSettingsTestCase(SmartSettingTestMixin, BaseTestCase):
    def test_setting_documentimagecache_storage_arguments_invalid_value(self):
        self._set_environment_variable(
            name='MAYAN_{}'.format(
                setting_documentimagecache_storage_arguments.global_name
            ), value="invalid_value"
        )
        self.test_case_silenced_logger_new_level = logging.FATAL + 10

        self._silence_logger(name='mayan.apps.documents.storages')

        with self.assertRaises(TypeError) as assertion:
            importlib.reload(storages)

        self.assertTrue('Unable to initialize' in str(assertion.exception))

    def test_setting_storage_backend_arguments_invalid_value(self):
        self._set_environment_variable(
            name='MAYAN_{}'.format(
                setting_storage_backend_arguments.global_name
            ), value="invalid_value"
        )
        self.test_case_silenced_logger_new_level = logging.FATAL + 10

        self._silence_logger(name='mayan.apps.documents.storages')

        with self.assertRaises(TypeError) as assertion:
            importlib.reload(storages)

        self.assertTrue('Unable to initialize' in str(assertion.exception))
