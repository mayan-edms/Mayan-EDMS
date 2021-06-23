from django.test import override_settings

from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..events import (
    event_file_metadata_document_file_submitted,
    event_file_metadata_document_file_finished
)
from ..permissions import (
    permission_document_type_file_metadata_setup,
    permission_file_metadata_submit, permission_file_metadata_view
)

from .literals import TEST_FILE_METADATA_KEY
from .mixins import DocumentTypeViewsTestMixin, FileMetadataViewsTestMixin


class DocumentTypeViewsTestCase(
    DocumentTypeViewsTestMixin, GenericDocumentViewTestCase
):
    def test_document_type_settings_view_no_permission(self):
        self._clear_events()

        response = self._request_document_type_settings_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_settings_view_with_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_file_metadata_setup
        )

        self._clear_events()

        response = self._request_document_type_settings_view()
        self.assertEqual(response.status_code, 200)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_submit_view_no_permission(self):
        file_metadata_driver_count = self.test_document.file_latest.file_metadata_drivers.count()

        self._clear_events()

        response = self._request_document_type_submit_view()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.test_document.file_latest.file_metadata_drivers.count(),
            file_metadata_driver_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_type_submit_view_with_access(self):
        self.grant_access(
            obj=self.test_document_type, permission=permission_file_metadata_submit
        )

        file_metadata_driver_count = self.test_document.file_latest.file_metadata_drivers.count()

        self._clear_events()

        response = self._request_document_type_submit_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_document.file_latest.file_metadata_drivers.count(),
            file_metadata_driver_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 2)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].action_object, self.test_document)
        self.assertEqual(events[0].target, self.test_document_file)
        self.assertEqual(
            events[0].verb, event_file_metadata_document_file_submitted.id
        )

        self.assertEqual(events[1].actor, self._test_case_user)
        self.assertEqual(events[1].action_object, self.test_document)
        self.assertEqual(events[1].target, self.test_document_file)
        self.assertEqual(
            events[1].verb, event_file_metadata_document_file_finished.id
        )

    def test_trashed_document_document_type_submit_view_with_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_file_metadata_submit
        )

        self.test_document.delete()

        file_metadata_driver_count = self.test_document.file_latest.file_metadata_drivers.count()

        self._clear_events()

        response = self._request_document_type_submit_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_document.file_latest.file_metadata_drivers.count(),
            file_metadata_driver_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


@override_settings(FILE_METADATA_AUTO_PROCESS=True)
class FileMetadataViewsTestCase(
    FileMetadataViewsTestMixin, GenericDocumentViewTestCase
):
    def setUp(self):
        super().setUp()
        self.test_driver = self.test_document.file_latest.file_metadata_drivers.first()

    def test_document_file_driver_list_view_no_permission(self):
        self._clear_events()

        response = self._request_document_file_driver_list_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_driver_list_view_with_access(self):
        self.grant_access(
            permission=permission_file_metadata_view, obj=self.test_document
        )

        self._clear_events()

        response = self._request_document_file_driver_list_view()
        self.assertContains(
            response=response, text=self.test_document.label, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_file_driver_list_view_with_access(self):
        self.grant_access(
            permission=permission_file_metadata_view, obj=self.test_document
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_document_file_driver_list_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_file_metadata_list_view_no_permission(self):
        self._clear_events()

        response = self._request_document_file_file_metadata_list_view()
        self.assertNotContains(
            response=response, text=TEST_FILE_METADATA_KEY, status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_file_file_metadata_list_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_file_metadata_view
        )

        self._clear_events()

        response = self._request_document_file_file_metadata_list_view()
        self.assertContains(
            response=response, text=TEST_FILE_METADATA_KEY, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_version_file_metadata_list_view_with_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_file_metadata_view
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_document_file_file_metadata_list_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_submit_view_no_permission(self):
        self.test_document.file_latest.file_metadata_drivers.all().delete()

        file_metadata_driver_count = self.test_document.file_latest.file_metadata_drivers.count()

        self._clear_events()

        response = self._request_document_file_submit_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_document.file_latest.file_metadata_drivers.count(),
            file_metadata_driver_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_submit_view_with_access(self):
        self.test_document.file_latest.file_metadata_drivers.all().delete()
        self.grant_access(
            permission=permission_file_metadata_submit, obj=self.test_document
        )

        file_metadata_driver_count = self.test_document.file_latest.file_metadata_drivers.count()

        self._clear_events()

        response = self._request_document_file_submit_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_document.file_latest.file_metadata_drivers.count(),
            file_metadata_driver_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 2)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].action_object, self.test_document)
        self.assertEqual(events[0].target, self.test_document_file)
        self.assertEqual(
            events[0].verb, event_file_metadata_document_file_submitted.id
        )

        self.assertEqual(events[1].actor, self._test_case_user)
        self.assertEqual(events[1].action_object, self.test_document)
        self.assertEqual(events[1].target, self.test_document_file)
        self.assertEqual(
            events[1].verb, event_file_metadata_document_file_finished.id
        )

    def test_trashed_document_submit_view_with_access(self):
        self.test_document.file_latest.file_metadata_drivers.all().delete()

        self.grant_access(
            permission=permission_file_metadata_submit, obj=self.test_document
        )

        file_metadata_driver_count = self.test_document.file_latest.file_metadata_drivers.count()

        self.test_document.delete()

        self._clear_events()

        response = self._request_document_file_submit_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_document.file_latest.file_metadata_drivers.count(),
            file_metadata_driver_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_multiple_document_submit_view_no_permission(self):
        self.test_document.file_latest.file_metadata_drivers.all().delete()

        file_metadata_driver_count = self.test_document.file_latest.file_metadata_drivers.count()

        self._clear_events()

        response = self._request_document_file_multiple_submit_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_document.file_latest.file_metadata_drivers.count(),
            file_metadata_driver_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_multiple_document_submit_view_with_access(self):
        self.test_document.file_latest.file_metadata_drivers.all().delete()
        self.grant_access(
            permission=permission_file_metadata_submit, obj=self.test_document
        )

        file_metadata_driver_count = self.test_document.file_latest.file_metadata_drivers.count()

        self._clear_events()

        response = self._request_document_file_multiple_submit_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_document.file_latest.file_metadata_drivers.count(),
            file_metadata_driver_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 2)

        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].action_object, self.test_document)
        self.assertEqual(events[0].target, self.test_document_file)
        self.assertEqual(
            events[0].verb, event_file_metadata_document_file_submitted.id
        )

        self.assertEqual(events[1].actor, self._test_case_user)
        self.assertEqual(events[1].action_object, self.test_document)
        self.assertEqual(events[1].target, self.test_document_file)
        self.assertEqual(
            events[1].verb, event_file_metadata_document_file_finished.id
        )

    def test_trashed_document_multiple_document_submit_view_with_access(self):
        self.test_document.file_latest.file_metadata_drivers.all().delete()

        self.grant_access(
            permission=permission_file_metadata_submit, obj=self.test_document
        )

        file_metadata_driver_count = self.test_document.file_latest.file_metadata_drivers.count()

        self.test_document.delete()

        self._clear_events()

        response = self._request_document_file_multiple_submit_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_document.file_latest.file_metadata_drivers.count(),
            file_metadata_driver_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
