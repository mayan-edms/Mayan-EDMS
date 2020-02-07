from __future__ import unicode_literals

from mayan.apps.common.tests.base import BaseTestCase
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
