from __future__ import unicode_literals

import importlib
import logging

from mayan.apps.common.tests.base import BaseTestCase
from mayan.apps.document_signatures import storages
from mayan.apps.smart_settings.tests.mixins import SmartSettingTestMixin

from ..settings import setting_storage_backend_arguments


class SignatureStorageSettingsTestCase(SmartSettingTestMixin, BaseTestCase):
    def test_setting_storage_backend_arguments_invalid_value(self):
        self._set_environment_variable(
            name='MAYAN_{}'.format(
                setting_storage_backend_arguments.global_name
            ), value="invalid_value"
        )
        self.test_case_silenced_logger_new_level = logging.FATAL + 10

        self._silence_logger(name='mayan.apps.document_signatures.storages')

        with self.assertRaises(TypeError) as assertion:
            importlib.reload(storages)

        self.assertTrue('Unable to initialize' in str(assertion.exception))
