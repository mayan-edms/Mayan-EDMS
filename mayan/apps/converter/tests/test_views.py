from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType

from mayan.apps.documents.tests import GenericDocumentViewTestCase

from ..models import Transformation
from ..permissions import (
    permission_transformation_create, permission_transformation_delete,
    permission_transformation_view
)

from .literals import TEST_TRANSFORMATION_NAME, TEST_TRANSFORMATION_ARGUMENT


class TransformationViewsTestCase(GenericDocumentViewTestCase):
    def _transformation_create_view(self):
        return self.post(
            viewname='converter:transformation_create', kwargs={
                'app_label': 'documents', 'model': 'document',
                'object_id': self.test_document.pk
            }, data={
                'name': TEST_TRANSFORMATION_NAME,
                'arguments': TEST_TRANSFORMATION_ARGUMENT
            }
        )

    def test_transformation_create_view_no_permissions(self):
        transformation_count = Transformation.objects.count()

        response = self._transformation_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(Transformation.objects.count(), transformation_count)

    def test_transformation_create_view_with_permissions(self):
        self.grant_permission(permission=permission_transformation_create)

        transformation_count = Transformation.objects.count()

        response = self._transformation_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            Transformation.objects.count(), transformation_count + 1
        )

    def _request_transformation_delete_view(self):
        return self.post(
            viewname='converter:transformation_delete', kwargs={
                'pk': self.test_transformation.pk
            }
        )

    def _create_test_transformation(self):
        content_type = ContentType.objects.get_for_model(model=self.test_document)

        self.test_transformation = Transformation.objects.create(
            content_type=content_type, object_id=self.test_document.pk,
            name=TEST_TRANSFORMATION_NAME,
            arguments=TEST_TRANSFORMATION_ARGUMENT
        )

    def test_transformation_delete_view_no_permissions(self):
        self._create_test_transformation()

        transformation_count = Transformation.objects.count()

        response = self._request_transformation_delete_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(
            Transformation.objects.count(), transformation_count
        )

    def test_transformation_delete_view_with_permissions(self):
        self._create_test_transformation()

        self.grant_permission(permission=permission_transformation_delete)

        transformation_count = Transformation.objects.count()

        response = self._request_transformation_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            Transformation.objects.count(), transformation_count - 1
        )

    def _transformation_list_view(self):
        return self.get(
            viewname='converter:transformation_list', kwargs={
                'app_label': 'documents', 'model': 'document',
                'object_id': self.test_document.pk
            }
        )

    def test_transformation_list_view_no_permissions(self):
        response = self._transformation_list_view()
        self.assertEqual(response.status_code, 403)

    def test_transformation_list_view_with_permissions(self):
        self.grant_access(
            obj=self.test_document, permission=permission_transformation_view
        )

        response = self._transformation_list_view()
        self.assertContains(
            response=response, text=self.test_document.label, status_code=200
        )
