from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType

from rest_framework import status

from mayan.apps.documents.tests.mixins import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..permissions import permission_events_view

from .mixins import EventTypeTestMixin


class EventTypeNamespaceAPITestCase(EventTypeTestMixin, BaseAPITestCase):
    def setUp(self):
        super(EventTypeNamespaceAPITestCase, self).setUp()
        self._create_test_event_type()

    def test_evet_type_list_view(self):
        response = self.get(viewname='rest_api:event-type-list')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_type_namespace_list_view(self):
        response = self.get(viewname='rest_api:event-type-namespace-list')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_type_namespace_event_type_list_view(self):
        response = self.get(
            viewname='rest_api:event-type-namespace-event-type-list',
            kwargs={
                'name': self.test_event_type_namespace.name
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ObjectEventAPITestCase(DocumentTestMixin, BaseAPITestCase):
    auto_upload_document = False

    def setUp(self):
        super(ObjectEventAPITestCase, self).setUp()
        self.test_object = self.test_document_type

        content_type = ContentType.objects.get_for_model(model=self.test_object)

        self.view_arguments = {
            'app_label': content_type.app_label,
            'model': content_type.model,
            'object_id': self.test_object.pk
        }

    def _request_object_event_list_api_view(self):
        return self.get(
            viewname='rest_api:object-event-list',
            kwargs=self.view_arguments
        )

    def test_object_event_list_view_no_permission(self):
        response = self._request_object_event_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_object_event_list_view_with_access(self):
        self.grant_access(
            obj=self.test_object, permission=permission_events_view
        )
        response = self._request_object_event_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
