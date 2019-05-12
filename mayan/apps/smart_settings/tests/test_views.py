from __future__ import absolute_import, unicode_literals

from mayan.apps.common.tests import GenericViewTestCase

from ..permissions import permission_settings_view

from .mixins import SmartSettingTestMixin


class SmartSettingViewTestCase(SmartSettingTestMixin, GenericViewTestCase):
    def setUp(self):
        super(SmartSettingViewTestCase, self).setUp()
        self._create_test_settings_namespace()

    def _request_namespace_list_view(self):
        return self.get(viewname='settings:namespace_list')

    def _request_namespace_detail_view(self):
        return self.get(
            viewname='settings:namespace_detail', kwargs={
                'namespace_name': self.test_settings_namespace.name
            }
        )

    def test_namespace_list_view_no_permission(self):
        response = self._request_namespace_list_view()
        self.assertEqual(response.status_code, 403)

    def test_namespace_detail_view_no_permission(self):
        response = self._request_namespace_detail_view()
        self.assertEqual(response.status_code, 403)

    def test_namespace_list_view_with_permission(self):
        self.grant_permission(permission=permission_settings_view)
        response = self._request_namespace_list_view()
        self.assertEqual(response.status_code, 200)

    def test_namespace_detail_view_with_permission(self):
        self.grant_permission(permission=permission_settings_view)
        response = self._request_namespace_detail_view()
        self.assertEqual(response.status_code, 200)
