from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.utils.encoding import force_bytes

from mayan.apps.common.tests.mixins import EnvironmentTestCaseMixin
from mayan.apps.storage.utils import fs_cleanup, NamedTemporaryFile

from ..classes import Namespace, Setting
from ..utils import BaseSetting, SettingNamespaceSingleton

from .literals import (
    TEST_BOOTSTAP_SETTING_NAME, TEST_NAMESPACE_LABEL, TEST_NAMESPACE_NAME,
    TEST_SETTING_DEFAULT_VALUE, TEST_SETTING_GLOBAL_NAME
)


class BoostrapSettingTestMixin(object):
    def _create_test_bootstrap_singleton(self):
        self.test_globals = {}
        self.test_globals['BASE_DIR'] = ''
        self.test_setting_namespace_singleton = SettingNamespaceSingleton(
            global_symbol_table=self.test_globals
        )

    def _register_test_boostrap_setting(self):
        SettingNamespaceSingleton.register_setting(
            name=TEST_BOOTSTAP_SETTING_NAME, klass=BaseSetting, kwargs={
                'has_default': True, 'default_value': 'value default'
            }
        )


class SmartSettingsTestCaseMixin(object):
    def setUp(self):
        super(SmartSettingsTestCaseMixin, self).setUp()
        Namespace.invalidate_cache_all()


class SmartSettingTestMixin(EnvironmentTestCaseMixin):
    test_setting_global_name = None
    test_config_file_object = None

    def tearDown(self):
        if self.test_config_file_object:
            fs_cleanup(filename=self.test_config_file_object.name)
        super(SmartSettingTestMixin, self).tearDown()

    def _create_test_config_file(self, callback=None):
        if not self.test_setting_global_name:
            self.test_setting_global_name = self.test_setting.global_name

        test_config_entry = {
            self.test_setting_global_name: self.test_config_value
        }

        with NamedTemporaryFile(delete=False) as test_config_file_object:
            # Needed to load the config file from the Setting class
            # after bootstrap.
            settings.CONFIGURATION_FILEPATH = test_config_file_object.name
            # Needed to update the globals before Mayan has loaded.
            self._set_environment_variable(
                name='MAYAN_CONFIGURATION_FILEPATH',
                value=test_config_file_object.name
            )
            test_config_file_object.write(
                force_bytes(
                    Setting.serialize_value(value=test_config_entry)
                )
            )
            test_config_file_object.seek(0)
            Setting._config_file_cache = None

            if callback:
                callback()

    def _create_test_settings_namespace(self, **kwargs):
        try:
            self.test_settings_namespace = Namespace.get(
                name=TEST_NAMESPACE_NAME
            )
            self.test_settings_namespace.migration_class = None
            self.test_settings_namespace.version = None
            self.test_settings_namespace.__dict__.update(kwargs)
        except KeyError:
            self.test_settings_namespace = Namespace(
                label=TEST_NAMESPACE_LABEL, name=TEST_NAMESPACE_NAME,
                **kwargs
            )

    def _create_test_setting(self):
        self.test_setting = self.test_settings_namespace.add_setting(
            global_name=TEST_SETTING_GLOBAL_NAME,
            default=TEST_SETTING_DEFAULT_VALUE
        )


class SmartSettingViewTestMixin(object):
    def _request_namespace_list_view(self):
        return self.get(viewname='settings:namespace_list')

    def _request_namespace_detail_view(self):
        return self.get(
            viewname='settings:namespace_detail', kwargs={
                'namespace_name': self.test_settings_namespace.name
            }
        )
