from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import (
    event_document_file_created, event_document_file_deleted,
    event_document_file_downloaded
)
from ..permissions import (
    permission_document_file_delete, permission_document_file_download,
    permission_document_file_new, permission_document_file_view
)

from .mixins.document_mixins import DocumentTestMixin
from .mixins.document_file_mixins import (
    DocumentFileTestMixin, DocumentFileAPIViewTestMixin
)


class DocumentFileAPIViewTestCase(
    DocumentFileAPIViewTestMixin, DocumentTestMixin,
    DocumentFileTestMixin, BaseAPITestCase
):
    _test_event_object_name = 'test_document_file'
    auto_upload_test_document = False

    def test_document_file_delete_api_view_no_permission(self):
        self._upload_test_document()
        self._upload_new_file()

        document_file_count = self.test_document.files.count()

        self._clear_events()

        response = self._request_test_document_file_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_document.files.count(), document_file_count
        )

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_document_file_delete_api_view_with_access(self):
        self._upload_test_document()
        self._upload_new_file()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_delete
        )

        document_file_count = self.test_document.files.count()

        self._clear_events()

        response = self._request_test_document_file_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(
            self.test_document.files.count(), document_file_count - 1
        )

        self.assertEqual(
            self.test_document.files.first(), self.test_document.file_latest
        )

        event = self._get_test_object_event(object_name='test_document')
        self.assertEqual(event.actor, self._test_case_user)
        self.assertEqual(event.target, self.test_document)
        self.assertEqual(event.verb, event_document_file_deleted.id)

    def test_document_file_detail_api_view_no_permission(self):
        self._upload_test_document()

        self._clear_events()

        response = self._request_test_document_file_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_document_file_detail_api_view_with_access(self):
        self._upload_test_document()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_view
        )

        self._clear_events()

        response = self._request_test_document_file_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data['checksum'], self.test_document.file_latest.checksum
        )

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_document_file_download_api_view_no_permission(self):
        self._upload_test_document()

        self._clear_events()

        response = self._request_test_document_file_download_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_document_file_download_api_view_with_access(self):
        self._upload_test_document()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_file_download
        )

        self._clear_events()

        response = self._request_test_document_file_download_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        with self.test_document.file_latest.open() as file_object:
            self.assert_download_response(
                response=response, content=file_object.read(),
                filename=self.test_document.file_latest.filename,
                mime_type=self.test_document.file_latest.mimetype
            )

        event = self._get_test_object_event()
        self.assertEqual(event.actor, self._test_case_user)
        self.assertEqual(event.target, self.test_document_file)
        self.assertEqual(event.verb, event_document_file_downloaded.id)

    def test_document_file_list_api_view_no_permission(self):
        self._upload_test_document()

        self._clear_events()

        response = self._request_test_document_file_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_document_file_list_api_view_with_access(self):
        self._upload_test_document()

        self.grant_access(
            obj=self.test_document, permission=permission_document_file_view
        )

        self._clear_events()

        response = self._request_test_document_file_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data['results'][0]['checksum'],
            self.test_document.file_latest.checksum
        )

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_document_file_upload_api_view_no_permission(self):
        self._upload_test_document()

        document_file_count = self.test_document.files.count()

        self._clear_events()

        response = self._request_test_document_file_upload_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_document.files.count(), document_file_count
        )

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_document_file_upload_api_view_with_access(self):
        self._upload_test_document()

        self.grant_access(
            obj=self.test_document, permission=permission_document_file_new
        )

        document_file_count = self.test_document.files.count()

        self._clear_events()

        response = self._request_test_document_file_upload_api_view()
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        self.assertEqual(
            self.test_document.files.count(), document_file_count + 1
        )

        self.assertEqual(self.test_document.file_latest.exists(), True)
        self.assertEqual(self.test_document.file_latest.size, 17436)
        self.assertEqual(
            self.test_document.file_latest.mimetype, 'image/png'
        )
        self.assertEqual(self.test_document.file_latest.encoding, 'binary')
        self.assertEqual(
            self.test_document.file_latest.checksum,
            'efa10e6cc21f83078aaa94d5cbe51de67b51af706143bafc7fd6d4c02124879a'
        )
        self.assertEqual(self.test_document.pages.count(), 1)

        event = self._get_test_object_event()
        self.assertEqual(event.actor, self._test_case_user)
        self.assertEqual(event.action_object, self.test_document)
        self.assertEqual(event.target, self.test_document_file)
        self.assertEqual(event.verb, event_document_file_created.id)
