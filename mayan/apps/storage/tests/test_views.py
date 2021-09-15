from django.utils.encoding import force_text

from mayan.apps.testing.tests.base import GenericViewTestCase

from ..events import (
    event_download_file_deleted, event_download_file_downloaded
)
from ..models import DownloadFile

from .literals import TEST_CONTENT
from .mixins import DownloadFileTestMixin, DownloadFileViewTestMixin


class DownloadFileViewTestCase(
    DownloadFileTestMixin, DownloadFileViewTestMixin, GenericViewTestCase
):
    def test_download_file_no_permission_delete_view(self):
        self._create_test_download_file()

        download_file_count = DownloadFile.objects.count()

        self._clear_events()

        response = self._request_test_download_file_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            DownloadFile.objects.count(), download_file_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, None)
        self.assertEqual(events[0].verb, event_download_file_deleted.id)

    def test_download_file_no_permission_with_content_object_delete_view(self):
        self._create_test_object()
        DownloadFile.objects.register_content_object(model=self.TestModel)
        self._create_test_download_file(content_object=self.test_object)

        download_file_count = DownloadFile.objects.count()

        self._clear_events()

        response = self._request_test_download_file_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            DownloadFile.objects.count(), download_file_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_object)
        self.assertEqual(events[0].verb, event_download_file_deleted.id)

    def test_download_file_with_permission_delete_view_no_permission(self):
        self._create_test_download_file_with_permission()

        download_file_count = DownloadFile.objects.count()

        self._clear_events()

        response = self._request_test_download_file_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            DownloadFile.objects.count(), download_file_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_download_file_with_permission_delete_view_with_access(self):
        self._create_test_download_file_with_permission()

        self.grant_access(
            obj=self.test_download_file,
            permission=self.test_permission
        )

        download_file_count = DownloadFile.objects.count()

        self._clear_events()

        response = self._request_test_download_file_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            DownloadFile.objects.count(), download_file_count - 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, None)
        self.assertEqual(events[0].verb, event_download_file_deleted.id)

    def test_download_file_no_permission_download_view(self):
        # Set the expected_content_types for
        # common.tests.mixins.ContentTypeCheckMixin
        self.expected_content_types = ('text/plain',)

        self._create_test_download_file(content=TEST_CONTENT)

        self._clear_events()

        response = self._request_test_download_file_download_view()
        self.assertEqual(response.status_code, 200)

        with self.test_download_file.open(mode='r') as file_object:
            self.assert_download_response(
                response=response, content=file_object.read(),
                filename=force_text(s=self.test_download_file),
                mime_type='text/plain'
            )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_download_file)
        self.assertEqual(events[0].verb, event_download_file_downloaded.id)

    def test_download_file_with_permission_download_view_no_permission(self):
        self._create_test_download_file_with_permission(content=TEST_CONTENT)

        self._clear_events()

        response = self._request_test_download_file_download_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_download_file_with_permission_download_view_with_access(self):
        # Set the expected_content_types for
        # common.tests.mixins.ContentTypeCheckMixin
        self.expected_content_types = ('text/plain',)

        self._create_test_download_file_with_permission(content=TEST_CONTENT)

        self.grant_access(
            obj=self.test_download_file,
            permission=self.test_permission
        )

        self._clear_events()

        response = self._request_test_download_file_download_view()
        self.assertEqual(response.status_code, 200)

        with self.test_download_file.open(mode='r') as file_object:
            self.assert_download_response(
                response=response, content=file_object.read(),
                filename=force_text(s=self.test_download_file),
                mime_type='text/plain'
            )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_download_file)
        self.assertEqual(events[0].verb, event_download_file_downloaded.id)

    def test_download_file_no_permission_list_view(self):
        self._create_test_download_file()

        self._clear_events()

        response = self._request_test_download_file_list_view()

        self.assertContains(
            response=response, text=str(self.test_download_file),
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_download_file_with_permission_list_view_no_permission(self):
        self._create_test_download_file_with_permission()

        self._clear_events()

        response = self._request_test_download_file_list_view()

        self.assertNotContains(
            response=response, text=str(self.test_download_file),
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_download_file_with_permission_list_view_with_access(self):
        self._create_test_download_file_with_permission()

        self.grant_access(
            obj=self.test_download_file,
            permission=self.test_permission
        )

        self._clear_events()

        response = self._request_test_download_file_list_view()

        self.assertContains(
            response=response, text=str(self.test_download_file),
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
