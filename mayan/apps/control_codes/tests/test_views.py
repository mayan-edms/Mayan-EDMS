from __future__ import unicode_literals

from django.test import override_settings

from mayan.apps.common.tests.base import BaseTestCase, GenericViewTestCase
from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.documents.tests.mixins import DocumentTestMixin

from ..classes import ControlCode
from ..models import ControlSheet
from ..permissions import (
    permission_control_sheet_create, permission_control_sheet_delete,
    permission_control_sheet_edit, permission_control_sheet_view
)

from .mixins import ControlSheetTestMixin, ControlSheetViewTestMixin


class ControlSheetViewTestCase(
    ControlSheetTestMixin, ControlSheetViewTestMixin, GenericViewTestCase
):
    test_model = ControlSheet
    test_permission_create = permission_control_sheet_create
    test_permission_delete = permission_control_sheet_delete

    def test_control_sheet_create_view_no_permissions(self):
        object_count = self.test_model.objects.count()

        response = self._request_test_control_sheet_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(self.test_model.objects.count(), object_count)

    def test_control_sheet_create_view_with_permissions(self):
        self.grant_permission(permission=self.test_permission_create)

        object_count = self.test_model.objects.count()

        response = self._request_test_control_sheet_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(self.test_model.objects.count(), object_count + 1)

    def test_control_sheet_delete_view_no_permissions(self):
        self._create_test_control_sheet()

        object_count = self.test_model.objects.count()

        response = self._request_test_control_sheet_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(self.test_model.objects.count(), object_count)

    def test_control_sheet_delete_view_with_access(self):
        self._create_test_control_sheet()

        self.grant_access(
            obj=self.test_control_sheet, permission=self.test_permission_delete
        )

        object_count = self.test_model.objects.count()

        response = self._request_test_control_sheet_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(self.test_model.objects.count(), object_count - 1)
