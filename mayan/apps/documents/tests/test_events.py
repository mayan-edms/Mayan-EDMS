from __future__ import unicode_literals

from actstream.models import Action
from django_downloadview import assert_download_response

from ..events import event_document_download, event_document_view
from ..permissions import (
    permission_document_download, permission_document_view
)

from .base import GenericDocumentViewTestCase


TEST_DOCUMENT_TYPE_EDITED_LABEL = 'test document type edited label'
TEST_DOCUMENT_TYPE_2_LABEL = 'test document type 2 label'
TEST_TRANSFORMATION_NAME = 'rotate'
TEST_TRANSFORMATION_ARGUMENT = 'degrees: 180'


class DocumentEventsTestCase(GenericDocumentViewTestCase):
    def _request_test_document_download_view(self):
        return self.get(
            'documents:document_download', kwargs={'pk': self.test_document.pk}
        )

    def test_document_download_event_no_permissions(self):
        Action.objects.all().delete()

        response = self._request_test_document_download_view()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(list(Action.objects.any(obj=self.test_document)), [])

    def test_document_download_event_with_permissions(self):
        self.expected_content_type = 'image/png; charset=utf-8'

        Action.objects.all().delete()

        self.grant_access(
            obj=self.test_document, permission=permission_document_download
        )

        response = self._request_test_document_download_view()

        # Download the file to close the file descriptor
        with self.test_document.open() as file_object:
            assert_download_response(
                self, response, content=file_object.read(),
                mime_type=self.test_document.file_mimetype
            )

        event = Action.objects.any(obj=self.test_document).first()

        self.assertEqual(event.actor, self._test_case_user)
        self.assertEqual(event.target, self.test_document)
        self.assertEqual(event.verb, event_document_download.id)

    def _request_test_document_preview_view(self):
        return self.get(
            viewname='documents:document_preview', kwargs={
                'pk': self.test_document.pk
            }
        )

    def test_document_view_event_no_permissions(self):
        Action.objects.all().delete()

        response = self._request_test_document_preview_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(list(Action.objects.any(obj=self.test_document)), [])

    def test_document_view_event_with_permissions(self):
        Action.objects.all().delete()

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_document_preview_view()
        self.assertEqual(response.status_code, 200)

        event = Action.objects.any(obj=self.test_document).first()
        self.assertEqual(event.actor, self._test_case_user)
        self.assertEqual(event.target, self.test_document)
        self.assertEqual(event.verb, event_document_view.id)
