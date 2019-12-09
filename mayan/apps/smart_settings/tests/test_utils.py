from __future__ import absolute_import, unicode_literals

from mayan.apps.common.tests.base import BaseTestCase
from mayan.apps.common.tests.mixins import EnvironmentTestCaseMixin

from .literals import (
    TEST_BOOTSTAP_SETTING_NAME, TEST_SETTING_VALUE,
    TEST_SETTING_VALUE_OVERRIDE
)
from .mixins import BoostrapSettingTestMixin


class BoostrapSettingTestCase(
    BoostrapSettingTestMixin, EnvironmentTestCaseMixin, BaseTestCase
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

        self._create_test_config_file(value=TEST_SETTING_VALUE)

        self.assertEqual(
            self.test_globals[TEST_BOOTSTAP_SETTING_NAME],
            TEST_SETTING_VALUE_OVERRIDE
        )

    def test_bootstrap_config_overrides_settings(self):
        self.test_globals[TEST_BOOTSTAP_SETTING_NAME] = TEST_SETTING_VALUE

        self._create_test_config_file(value=TEST_SETTING_VALUE_OVERRIDE)

        self.assertEqual(
            self.test_globals[TEST_BOOTSTAP_SETTING_NAME],
            TEST_SETTING_VALUE_OVERRIDE
        )

    def test_bootstrap_settings_overrides_default(self):
        self.test_globals[
            TEST_BOOTSTAP_SETTING_NAME
        ] = TEST_SETTING_VALUE_OVERRIDE

        self.setting_namespace.update_globals()

        self.assertEqual(
            self.test_globals[TEST_BOOTSTAP_SETTING_NAME],
            TEST_SETTING_VALUE_OVERRIDE
        )

    def test_bootstrap_default(self):
        self.setting_namespace.update_globals()

        self.assertEqual(
            self.test_globals[TEST_BOOTSTAP_SETTING_NAME], 'value default'
        )
