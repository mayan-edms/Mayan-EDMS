from __future__ import absolute_import, unicode_literals

from mayan.apps.common.tests.base import BaseTestCase

from .literals import (
    TEST_BOOTSTAP_SETTING_NAME, TEST_SETTING_VALUE,
    TEST_SETTING_VALUE_OVERRIDE
)
from .mixins import BoostrapSettingTestMixin, SmartSettingTestMixin


class BoostrapSettingTestCase(
    BoostrapSettingTestMixin, SmartSettingTestMixin, BaseTestCase
):
    def setUp(self):
        super(BoostrapSettingTestCase, self).setUp()
        self._register_test_boostrap_setting()
        self._create_test_bootstrap_singleton()

    def test_bootstrap_environment_overrides_config(self):
        self._set_environment_variable(
            name='MAYAN_{}'.format(TEST_BOOTSTAP_SETTING_NAME),
            value=TEST_SETTING_VALUE_OVERRIDE
        )

        self.test_setting_global_name = TEST_BOOTSTAP_SETTING_NAME
        self.test_config_value = TEST_SETTING_VALUE
        self._create_test_config_file(
            callback=self.test_setting_namespace_singleton.update_globals
        )

        self.assertEqual(
            self.test_globals[TEST_BOOTSTAP_SETTING_NAME],
            TEST_SETTING_VALUE_OVERRIDE
        )

    def test_bootstrap_config_overrides_settings(self):
        self.test_globals[TEST_BOOTSTAP_SETTING_NAME] = TEST_SETTING_VALUE

        self.test_setting_global_name = TEST_BOOTSTAP_SETTING_NAME
        self.test_config_value = TEST_SETTING_VALUE_OVERRIDE
        self._create_test_config_file(
            callback=self.test_setting_namespace_singleton.update_globals
        )

        self.assertEqual(
            self.test_globals[TEST_BOOTSTAP_SETTING_NAME],
            TEST_SETTING_VALUE_OVERRIDE
        )

    def test_bootstrap_settings_overrides_default(self):
        self.test_globals[
            TEST_BOOTSTAP_SETTING_NAME
        ] = TEST_SETTING_VALUE_OVERRIDE

        self.test_setting_namespace_singleton.update_globals()

        self.assertEqual(
            self.test_globals[TEST_BOOTSTAP_SETTING_NAME],
            TEST_SETTING_VALUE_OVERRIDE
        )

    def test_bootstrap_default(self):
        self.test_setting_namespace_singleton.update_globals()

        self.assertEqual(
            self.test_globals[TEST_BOOTSTAP_SETTING_NAME], 'value default'
        )
