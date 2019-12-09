from __future__ import absolute_import, unicode_literals

from django.utils.encoding import force_bytes

from mayan.apps.storage.utils import NamedTemporaryFile

from ..classes import Namespace
from ..utils import BaseSetting, SettingNamespaceSingleton

from .literals import (
    TEST_BOOTSTAP_SETTING_NAME, TEST_NAMESPACE_LABEL, TEST_NAMESPACE_NAME,
    TEST_SETTING_DEFAULT_VALUE, TEST_SETTING_GLOBAL_NAME
)


class BoostrapSettingTestMixin(object):
    def _create_test_bootstrap_singleton(self):
        self.test_globals = {}
        self.test_globals['BASE_DIR'] = ''
        self.setting_namespace = SettingNamespaceSingleton(
            global_symbol_table=self.test_globals
        )

    def _create_test_config_file(self, value):
        with NamedTemporaryFile() as file_object:
            self._set_environment_variable(
                name='MAYAN_CONFIGURATION_FILEPATH',
                value=file_object.name
            )

            file_object.write(
                force_bytes(
                    '{}: {}'.format(
                        TEST_BOOTSTAP_SETTING_NAME, value
                    )
                )
            )
            file_object.seek(0)

            self.setting_namespace.update_globals()

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


class SmartSettingTestMixin(object):
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
