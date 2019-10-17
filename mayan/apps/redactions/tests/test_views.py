from __future__ import unicode_literals

from mayan.apps.converter.models import LayerTransformation
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..permissions import (
    permission_redaction_create, permission_redaction_delete,
    permission_redaction_edit, permission_redaction_exclude,
    permission_redaction_view
)

from .mixins import RedactionTestMixin, RedactionViewsTestMixin


class RedactionViewsTestCase(
    RedactionTestMixin, RedactionViewsTestMixin,
    GenericDocumentViewTestCase
):
    def test_redaction_create_view_no_permission(self):
        redaction_count = LayerTransformation.objects.count()

        response = self._request_redaction_create_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            LayerTransformation.objects.count(), redaction_count
        )

    def test_redaction_create_view_with_permission(self):
        self.grant_access(
            obj=self.test_document, permission=permission_redaction_create
        )

        redaction_count = LayerTransformation.objects.count()

        response = self._request_redaction_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            LayerTransformation.objects.count(), redaction_count + 1
        )

    def test_redaction_delete_view_no_permission(self):
        self._create_test_redaction()

        redaction_count = LayerTransformation.objects.count()

        response = self._request_redaction_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            LayerTransformation.objects.count(), redaction_count
        )

    def test_redaction_delete_view_with_access(self):
        self._create_test_redaction()

        self.grant_access(
            obj=self.test_document, permission=permission_redaction_delete
        )

        redaction_count = LayerTransformation.objects.count()

        response = self._request_redaction_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            LayerTransformation.objects.count(), redaction_count - 1
        )

    def test_redaction_edit_view_no_permission(self):
        self._create_test_redaction()

        redaction_arguments = self.test_redaction.arguments

        response = self._request_redaction_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_redaction.refresh_from_db()
        self.assertEqual(
            redaction_arguments, self.test_redaction.arguments
        )

    def test_redaction_edit_view_with_access(self):
        self._create_test_redaction()

        self.grant_access(
            obj=self.test_document, permission=permission_redaction_edit
        )

        redaction_arguments = self.test_redaction.arguments
        response = self._request_redaction_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_redaction.refresh_from_db()
        self.assertNotEqual(
            redaction_arguments, self.test_redaction.arguments
        )

    def test_redaction_list_view_no_permission(self):
        self._create_test_redaction()

        response = self._request_redaction_list_view()
        self.assertNotContains(
            response=response, text=self.test_document.label, status_code=404
        )
        self.assertNotContains(
            response=response,
            text=self.test_redaction.get_transformation_class().label,
            status_code=404
        )

    def test_redaction_list_view_with_access(self):
        self._create_test_redaction()

        self.grant_access(
            obj=self.test_document, permission=permission_redaction_view
        )

        response = self._request_redaction_list_view()
        self.assertContains(
            response=response, text=self.test_document.label, status_code=200
        )
        self.assertContains(
            response=response,
            text=self.test_redaction.get_transformation_class().label,
            status_code=200
        )
