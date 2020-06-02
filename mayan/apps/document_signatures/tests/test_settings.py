import importlib
import logging

from mayan.apps.tests.tests.base import BaseTestCase
from mayan.apps.document_signatures import storages
from mayan.apps.smart_settings.tests.mixins import SmartSettingTestMixin
from mayan.apps.storage.classes import DefinedStorage

from ..literals import STORAGE_NAME_DOCUMENT_SIGNATURES_DETACHED_SIGNATURE
from ..settings import setting_storage_backend_arguments


class SignatureStorageSettingsTestCase(SmartSettingTestMixin, BaseTestCase):
    def tearDown(self):
        super(SignatureStorageSettingsTestCase, self).tearDown()
        importlib.reload(storages)

    def test_setting_storage_backend_arguments_invalid_value(self):
        self._set_environment_variable(
            name='MAYAN_{}'.format(
                setting_storage_backend_arguments.global_name
            ), value="invalid_value"
        )

        self.test_case_silenced_logger_new_level = logging.FATAL + 10
        self._silence_logger(name='mayan.apps.storage.classes')

        with self.assertRaises(expected_exception=TypeError) as assertion:
            importlib.reload(storages)
            DefinedStorage.get(
                name=STORAGE_NAME_DOCUMENT_SIGNATURES_DETACHED_SIGNATURE
            ).get_storage_instance()
        self.assertTrue('Unable to initialize' in str(assertion.exception))
        self.assertTrue('detached signatures' in str(assertion.exception))
