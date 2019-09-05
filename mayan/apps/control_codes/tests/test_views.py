from __future__ import unicode_literals

from mayan.apps.common.tests.base import GenericViewTestCase

from ..models import ControlSheet, ControlSheetCode
from ..permissions import (
    permission_control_sheet_create, permission_control_sheet_delete,
    permission_control_sheet_edit, permission_control_sheet_view
)

from .mixins import (
    ControlSheetCodeTestMixin, ControlSheetCodeViewTestMixin,
    ControlSheetTestMixin, ControlSheetViewTestMixin
)


class ControlSheetViewTestCase(
    ControlSheetTestMixin, ControlSheetViewTestMixin, GenericViewTestCase
):
    _test_model = ControlSheet
    _test_permission_create = permission_control_sheet_create
    _test_permission_delete = permission_control_sheet_delete
    _test_permission_edit = permission_control_sheet_edit
    _test_permission_view = permission_control_sheet_view

    def test_control_sheet_create_view_no_permissions(self):
        object_count = self._test_model.objects.count()

        response = self._request_test_control_sheet_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(self._test_model.objects.count(), object_count)

    def test_control_sheet_create_view_with_permissions(self):
        self.grant_permission(permission=self._test_permission_create)

        object_count = self._test_model.objects.count()

        response = self._request_test_control_sheet_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(self._test_model.objects.count(), object_count + 1)

    def test_control_sheet_delete_view_no_permissions(self):
        self._create_test_control_sheet()

        object_count = self._test_model.objects.count()

        response = self._request_test_control_sheet_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(self._test_model.objects.count(), object_count)

    def test_control_sheet_delete_view_with_access(self):
        self._create_test_control_sheet()

        self.grant_access(
            obj=self.test_control_sheet, permission=self._test_permission_delete
        )

        object_count = self._test_model.objects.count()

        response = self._request_test_control_sheet_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(self._test_model.objects.count(), object_count - 1)

    def test_control_sheet_edit_view_no_permissions(self):
        self._create_test_control_sheet()

        control_sheet_label = self.test_control_sheet.label

        response = self._request_test_control_sheet_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_control_sheet.refresh_from_db()
        self.assertEqual(self.test_control_sheet.label, control_sheet_label)

    def test_control_sheet_edit_view_with_access(self):
        self._create_test_control_sheet()

        self.grant_access(
            obj=self.test_control_sheet, permission=self._test_permission_edit
        )

        control_sheet_label = self.test_control_sheet.label

        response = self._request_test_control_sheet_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_control_sheet.refresh_from_db()
        self.assertNotEqual(self.test_control_sheet.label, control_sheet_label)

    def test_control_sheet_list_view_no_permission(self):
        self._create_test_control_sheet()

        response = self._request_test_control_sheet_list_view()
        self.assertNotContains(
            response, text=self.test_control_sheet.label, status_code=200
        )

    def test_control_sheet_list_view_with_access(self):
        self._create_test_control_sheet()
        self.grant_access(
            obj=self.test_control_sheet,
            permission=self._test_permission_view
        )

        response = self._request_test_control_sheet_list_view()
        self.assertContains(
            response, text=self.test_control_sheet.label, status_code=200
        )

    def test_control_sheet_preview_view_no_permissions(self):
        self._create_test_control_sheet()

        response = self._request_test_control_sheet_preview_view()
        self.assertEqual(response.status_code, 404)

    def test_control_sheet_preview_view_with_access(self):
        self._create_test_control_sheet()

        self.grant_access(
            obj=self.test_control_sheet, permission=self._test_permission_view
        )

        response = self._request_test_control_sheet_preview_view()
        self.assertContains(
            response=response, text=self.test_control_sheet.label,
            status_code=200
        )

    def test_control_sheet_print_view_no_permissions(self):
        self._create_test_control_sheet()

        response = self._request_test_control_sheet_print_view()
        self.assertEqual(response.status_code, 404)

    def test_control_sheet_print_view_with_access(self):
        self._create_test_control_sheet()

        self.grant_access(
            obj=self.test_control_sheet, permission=self._test_permission_view
        )

        response = self._request_test_control_sheet_print_view()
        self.assertContains(
            response=response, text=self.test_control_sheet.label,
            status_code=200
        )


class ControlSheetCodeViewTestCase(
    ControlSheetTestMixin, ControlSheetCodeTestMixin,
    ControlSheetCodeViewTestMixin, GenericViewTestCase
):
    _test_model = ControlSheetCode
    _test_permission_create = permission_control_sheet_create
    _test_permission_delete = permission_control_sheet_delete
    _test_permission_edit = permission_control_sheet_edit
    _test_permission_view = permission_control_sheet_view

    def test_control_sheet_code_select_get_view_no_permissions(self):
        self._create_test_control_sheet()

        response = self._request_test_control_sheet_code_select_get_view()
        self.assertEqual(response.status_code, 404)

    def test_control_sheet_code_select_get_view_with_access(self):
        self._create_test_control_sheet()

        self.grant_access(
            obj=self.test_control_sheet,
            permission=self._test_permission_edit
        )

        response = self._request_test_control_sheet_code_select_get_view()

        self.assertContains(
            response=response, text=self._test_control_code_class.label,
            status_code=200
        )

    def test_control_sheet_code_select_post_view_no_permissions(self):
        self._create_test_control_sheet()

        response = self._request_test_control_sheet_code_select_post_view()
        self.assertEqual(response.status_code, 404)

    def test_control_sheet_code_select_post_view_with_access(self):
        self._create_test_control_sheet()

        self.grant_access(
            obj=self.test_control_sheet,
            permission=self._test_permission_edit
        )

        response = self._request_test_control_sheet_code_select_post_view()
        self.assertEqual(response.status_code, 302)

    def test_control_sheet_code_create_view_no_permissions(self):
        self._create_test_control_sheet()

        object_count = self._test_model.objects.count()

        response = self._request_test_control_sheet_code_create_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(self._test_model.objects.count(), object_count)

    def test_control_sheet_code_create_view_with_access(self):
        self._create_test_control_sheet()

        self.grant_access(
            obj=self.test_control_sheet,
            permission=self._test_permission_edit
        )

        object_count = self._test_model.objects.count()

        response = self._request_test_control_sheet_code_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(self._test_model.objects.count(), object_count + 1)

    def test_control_sheet_code_delete_view_no_permissions(self):
        self._create_test_control_sheet()
        self._create_test_control_sheet_code()

        object_count = self._test_model.objects.count()

        response = self._request_test_control_sheet_code_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(self._test_model.objects.count(), object_count)

    def test_control_sheet_code_delete_view_with_access(self):
        self._create_test_control_sheet()
        self._create_test_control_sheet_code()

        self.grant_access(
            obj=self.test_control_sheet,
            permission=self._test_permission_edit
        )

        object_count = self._test_model.objects.count()

        response = self._request_test_control_sheet_code_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(self._test_model.objects.count(), object_count - 1)

    def test_control_sheet_code_edit_view_no_permissions(self):
        self._create_test_control_sheet()
        self._create_test_control_sheet_code()

        control_sheet_code_arguments = self.test_control_sheet_code.arguments

        response = self._request_test_control_sheet_code_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_control_sheet_code.refresh_from_db()
        self.assertEqual(
            self.test_control_sheet_code.arguments,
            control_sheet_code_arguments
        )

    def test_control_sheet_code_edit_view_with_access(self):
        self._create_test_control_sheet()
        self._create_test_control_sheet_code()

        self.grant_access(
            obj=self.test_control_sheet,
            permission=self._test_permission_edit
        )

        control_sheet_code_arguments = self.test_control_sheet_code.arguments

        response = self._request_test_control_sheet_code_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_control_sheet_code.refresh_from_db()
        self.assertNotEqual(
            self.test_control_sheet_code.arguments,
            control_sheet_code_arguments
        )

    def test_control_sheet_code_list_view_no_permission(self):
        self._create_test_control_sheet()
        self._create_test_control_sheet_code()

        response = self._request_test_control_sheet_code_list_view()
        self.assertNotContains(
            response, text=self.test_control_sheet_code.get_label(),
            status_code=404
        )

    def test_control_sheet_code_list_view_with_access(self):
        self._create_test_control_sheet()
        self._create_test_control_sheet_code()
        self.grant_access(
            obj=self.test_control_sheet,
            permission=self._test_permission_view
        )

        response = self._request_test_control_sheet_code_list_view()
        self.assertContains(
            response, text=self.test_control_sheet_code.get_label(),
            status_code=200
        )
