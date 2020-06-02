from mayan.apps.tests.tests.base import GenericViewTestCase

from ..permissions import permission_settings_view

from .mixins import SmartSettingTestMixin, SmartSettingViewTestMixin


class SmartSettingViewTestCase(
    SmartSettingTestMixin, SmartSettingViewTestMixin, GenericViewTestCase
):
    def setUp(self):
        super(SmartSettingViewTestCase, self).setUp()
        self._create_test_settings_namespace()

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
