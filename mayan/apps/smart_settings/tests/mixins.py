from __future__ import absolute_import, unicode_literals

from ..classes import Namespace

from .literals import (
    TEST_NAMESPACE_LABEL, TEST_NAMESPACE_NAME, TEST_SETTING_DEFAULT_VALUE,
    TEST_SETTING_GLOBAL_NAME
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
