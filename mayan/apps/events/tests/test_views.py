from __future__ import absolute_import, unicode_literals

from django.contrib.contenttypes.models import ContentType

from mayan.apps.documents.tests import GenericDocumentViewTestCase

from ..permissions import permission_events_view


class EventsViewTestCase(GenericDocumentViewTestCase):
    def setUp(self):
        super(EventsViewTestCase, self).setUp()

        content_type = ContentType.objects.get_for_model(self.test_document)

        self.view_arguments = {
            'app_label': content_type.app_label,
            'model': content_type.model,
            'object_id': self.document.pk
        }

    def _request_events_for_object_view(self):
        return self.get(
            viewname='events:events_for_object', kwargs=self.view_arguments
        )

    def test_events_for_object_view_no_permission(self):
        response = self._request_events_for_object_view()
        self.assertNotContains(
            response=response, text=self.test_document.label, status_code=403
        )
        self.assertNotContains(
            response=response, text='otal:', status_code=403
        )

    def test_events_for_object_view_with_permission(self):
        self.grant_permission(permission=permission_events_view)

        response = self._request_events_for_object_view()
        self.assertContains(
            response=response, text=self.test_document.label, status_code=200
        )
        self.assertNotContains(
            response=response, text='otal: 0', status_code=200
        )
