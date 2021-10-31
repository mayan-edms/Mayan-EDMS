from mayan.apps.testing.tests.base import GenericViewTestCase

from ..permissions import permission_settings_edit, permission_settings_view

from .literals import (
    TEST_SETTING_VALIDATION_BAD_VALUE, TEST_SETTING_VALIDATION_GOOD_VALUE
)
from .mixins import (
    SmartSettingNamespaceTestMixin, SmartSettingNamespaceViewTestMixin,
    SmartSettingTestMixin, SmartSettingViewTestMixin
)
from .mocks import test_validation_function


class SmartSettingNamespaceViewTestCase(
    SmartSettingNamespaceTestMixin, SmartSettingNamespaceViewTestMixin,
    GenericViewTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_settings_namespace()

    def test_namespace_detail_view_no_permission(self):
        response = self._request_namespace_detail_view()
        self.assertEqual(response.status_code, 403)

    def test_namespace_detail_view_with_permission(self):
        self.grant_permission(permission=permission_settings_view)

        response = self._request_namespace_detail_view()
        self.assertEqual(response.status_code, 200)

    def test_namespace_list_view_no_permission(self):
        response = self._request_namespace_list_view()
        self.assertEqual(response.status_code, 403)

    def test_namespace_list_view_with_permission(self):
        self.grant_permission(permission=permission_settings_view)

        response = self._request_namespace_list_view()
        self.assertEqual(response.status_code, 200)


class SmartSettingViewTestCase(
    SmartSettingNamespaceTestMixin, SmartSettingTestMixin,
    SmartSettingViewTestMixin, GenericViewTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_settings_namespace()

    def test_setting_edit_view_no_permission(self):
        self._create_test_setting()

        test_setting_value = self.test_setting.value

        response = self._request_setting_edit_view(
            value=TEST_SETTING_VALIDATION_GOOD_VALUE
        )
        self.assertEqual(response.status_code, 403)

        self.assertEqual(
            self.test_setting.value, test_setting_value
        )

    def test_setting_edit_view_with_permission(self):
        self.grant_permission(permission=permission_settings_edit)

        self._create_test_setting()

        test_setting_value = self.test_setting.value

        response = self._request_setting_edit_view(
            value=TEST_SETTING_VALIDATION_GOOD_VALUE
        )
        self.assertEqual(response.status_code, 302)

        self.assertNotEqual(
            self.test_setting.value, test_setting_value
        )

    def test_setting_validation_with_permission(self):
        self.grant_permission(permission=permission_settings_edit)

        self._create_test_setting(
            validation_function=test_validation_function
        )

        test_setting_value = self.test_setting.value

        response = self._request_setting_edit_view(
            value=TEST_SETTING_VALIDATION_BAD_VALUE
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.test_setting.value, test_setting_value
        )
