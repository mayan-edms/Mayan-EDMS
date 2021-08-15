import importlib
import logging

from mayan.apps.smart_settings.tests.mixins import SmartSettingTestMixin
from mayan.apps.sources import storages
from mayan.apps.storage.classes import DefinedStorage
from mayan.apps.testing.tests.base import BaseTestCase

from ..literals import STORAGE_NAME_SOURCE_CACHE_FOLDER
from ..settings import setting_source_cache_storage_backend_arguments


class SourcesStorageSettingsTestCase(SmartSettingTestMixin, BaseTestCase):
    def tearDown(self):
        super().tearDown()
        importlib.reload(storages)

    def test_setting_source_cache_storage_backend_arguments_invalid_value(self):
        self._set_environment_variable(
            name='MAYAN_{}'.format(
                setting_source_cache_storage_backend_arguments.global_name
            ), value="invalid_value"
        )
        self.test_case_silenced_logger_new_level = logging.FATAL + 10
        self._silence_logger(name='mayan.apps.storage.classes')

        with self.assertRaises(expected_exception=TypeError) as assertion:
            importlib.reload(storages)
            DefinedStorage.get(
                name=STORAGE_NAME_SOURCE_CACHE_FOLDER
            ).get_storage_instance()
        self.assertTrue('Unable to initialize' in str(assertion.exception))
        self.assertTrue('staging folder' in str(assertion.exception))
