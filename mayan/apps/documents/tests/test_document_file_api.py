from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import (
    event_document_file_created, event_document_file_deleted,
    event_document_file_edited, event_document_file_downloaded,
    event_document_version_created, event_document_version_page_created
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

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

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

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)
        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_document_file_deleted.id)

    def test_document_file_detail_api_view_no_permission(self):
        self._upload_test_document()

        self._clear_events()

        response = self._request_test_document_file_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

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

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_download_api_view_no_permission(self):
        self._upload_test_document()

        self._clear_events()

        response = self._request_test_document_file_download_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

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

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)
        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document_file)
        self.assertEqual(events[0].verb, event_document_file_downloaded.id)

    def test_document_file_list_api_view_no_permission(self):
        self._upload_test_document()

        self._clear_events()

        response = self._request_test_document_file_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

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

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_upload_api_view_no_permission(self):
        self._upload_test_document()

        document_file_count = self.test_document.files.count()

        self._clear_events()

        response = self._request_test_document_file_upload_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_document.files.count(), document_file_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

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

        events = self._get_test_events()
        self.assertEqual(events.count(), 4)

        self.assertEqual(events[0].action_object, self.test_document)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document_file)
        self.assertEqual(events[0].verb, event_document_file_created.id)

        self.assertEqual(events[1].action_object, self.test_document)
        self.assertEqual(events[1].actor, self._test_case_user)
        self.assertEqual(events[1].target, self.test_document_file)
        self.assertEqual(events[1].verb, event_document_file_edited.id)

        self.test_document.refresh_from_db()
        test_document_version = self.test_document.versions.last()

        self.assertEqual(events[2].action_object, self.test_document)
        self.assertEqual(events[2].actor, self._test_case_user)
        self.assertEqual(events[2].target, test_document_version)
        self.assertEqual(events[2].verb, event_document_version_created.id)

        self.assertEqual(events[3].action_object, test_document_version)
        self.assertEqual(events[3].actor, self._test_case_user)
        self.assertEqual(events[3].target, test_document_version.pages.first())
        self.assertEqual(events[3].verb, event_document_version_page_created.id)
