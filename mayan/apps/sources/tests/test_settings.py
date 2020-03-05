from __future__ import unicode_literals

import importlib
import logging

from mayan.apps.common.tests.base import BaseTestCase
from mayan.apps.smart_settings.tests.mixins import SmartSettingTestMixin
from mayan.apps.sources import storages

from ..settings import setting_staging_file_image_cache_storage_arguments


class SourcesStorageSettingsTestCase(SmartSettingTestMixin, BaseTestCase):
    def test_setting_staging_file_image_cache_storage_arguments_invalid_value(self):
        self._set_environment_variable(
            name='MAYAN_{}'.format(
                setting_staging_file_image_cache_storage_arguments.global_name
            ), value="invalid_value"
        )
        self.test_case_silenced_logger_new_level = logging.FATAL + 10

        self._silence_logger(name='mayan.apps.sources.storages')

        with self.assertRaises(TypeError) as assertion:
            importlib.reload(storages)

        self.assertTrue('Unable to initialize' in str(assertion.exception))
