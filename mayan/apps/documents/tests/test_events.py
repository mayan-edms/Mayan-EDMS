from __future__ import unicode_literals

from actstream.models import Action

from ..events import (
    event_document_download, event_document_trashed, event_document_view
)
from ..permissions import (
    permission_document_download, permission_document_trash,
    permission_document_view
)

from .base import GenericDocumentViewTestCase
from .mixins import TrashedDocumentViewTestMixin

TEST_DOCUMENT_TYPE_EDITED_LABEL = 'test document type edited label'
TEST_DOCUMENT_TYPE_2_LABEL = 'test document type 2 label'
TEST_TRANSFORMATION_NAME = 'rotate'
TEST_TRANSFORMATION_ARGUMENT = 'degrees: 180'


class DocumentEventsTestMixin(object):
    def _request_test_document_download_view(self):
        return self.get(
            'documents:document_download', kwargs={'pk': self.test_document.pk}
        )

    def _request_test_document_preview_view(self):
        return self.get(
            viewname='documents:document_preview', kwargs={
                'pk': self.test_document.pk
            }
        )


class DocumentEventsTestCase(
    DocumentEventsTestMixin, TrashedDocumentViewTestMixin,
    GenericDocumentViewTestCase
):
    def setUp(self):
        super(DocumentEventsTestCase, self).setUp()
        Action.objects.all().delete()

    def test_document_download_event_no_permission(self):
        response = self._request_test_document_download_view()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(list(Action.objects.any(obj=self.test_document)), [])

    def test_document_download_event_with_access(self):
        self.expected_content_types = ('image/png',)

        self.grant_access(
            obj=self.test_document, permission=permission_document_download
        )

        response = self._request_test_document_download_view()

        # Download the file to close the file descriptor
        with self.test_document.open() as file_object:
            self.assert_download_response(
                response=response, content=file_object.read(),
                mime_type=self.test_document.file_mimetype
            )

        event = Action.objects.any(obj=self.test_document).first()

        self.assertEqual(event.actor, self._test_case_user)
        self.assertEqual(event.target, self.test_document)
        self.assertEqual(event.verb, event_document_download.id)

    def test_document_view_event_no_permission(self):
        response = self._request_test_document_preview_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(list(Action.objects.any(obj=self.test_document)), [])

    def test_document_view_event_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        response = self._request_test_document_preview_view()
        self.assertEqual(response.status_code, 200)

        event = Action.objects.any(obj=self.test_document).first()
        self.assertEqual(event.actor, self._test_case_user)
        self.assertEqual(event.target, self.test_document)
        self.assertEqual(event.verb, event_document_view.id)

    def test_document_trashed_view_event_no_permission(self):
        response = self._request_document_trash_post_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(list(Action.objects.any(obj=self.test_document)), [])

    def test_document_trashed_view_event_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_trash
        )

        response = self._request_document_trash_post_view()
        self.assertEqual(response.status_code, 302)

        event = Action.objects.any(obj=self.test_document).first()
        self.assertEqual(event.actor, self._test_case_user)
        self.assertEqual(event.target, self.test_document)
        self.assertEqual(event.verb, event_document_trashed.id)
