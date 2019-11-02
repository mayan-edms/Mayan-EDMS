from __future__ import absolute_import, unicode_literals

from ..classes import Namespace

from .literals import TEST_NAMESPACE_LABEL, TEST_NAMESPACE_NAME


class SmartSettingsTestCaseMixin(object):
    def setUp(self):
        super(SmartSettingsTestCaseMixin, self).setUp()
        Namespace.invalidate_cache_all()


class SmartSettingTestMixin(object):
    def _create_test_settings_namespace(self):
        try:
            self.test_settings_namespace = Namespace.get(
                name=TEST_NAMESPACE_NAME
            )
        except KeyError:
            self.test_settings_namespace = Namespace(
                label=TEST_NAMESPACE_LABEL, name=TEST_NAMESPACE_NAME
            )
