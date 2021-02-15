from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import (
    event_document_created, event_document_edited,
    event_document_file_created, event_document_file_edited,
    event_document_type_changed, event_document_version_created,
    event_document_version_page_created
)
from ..models.document_models import Document
from ..models.document_type_models import DocumentType
from ..permissions import (
    permission_document_create, permission_document_properties_edit,
    permission_document_view
)

from .literals import TEST_DOCUMENT_TYPE_2_LABEL
from .mixins.document_mixins import (
    DocumentAPIViewTestMixin, DocumentTestMixin
)


class DocumentAPIViewTestCase(
    DocumentAPIViewTestMixin, DocumentTestMixin, BaseAPITestCase
):
    auto_upload_test_document = False

    def test_document_create_api_view_no_permission(self):
        document_count = Document.objects.count()

        self._clear_events()

        response = self._request_test_document_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            Document.objects.count(), document_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_create_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_create
        )

        document_count = Document.objects.count()

        self._clear_events()

        response = self._request_test_document_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            Document.objects.count(), document_count + 1
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)
        self.assertEqual(events[0].action_object, self.test_document_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_document_created.id)

    def test_document_change_type_api_view_no_permission(self):
        self._upload_test_document()

        self.test_document_type_2 = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_2_LABEL
        )

        self._clear_events()

        response = self._request_test_document_change_type_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document.refresh_from_db()
        self.assertNotEqual(
            self.test_document.document_type,
            self.test_document_type_2
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_change_type_api_view_with_access(self):
        self._upload_test_document()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_properties_edit
        )
        self.test_document_type_2 = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_2_LABEL
        )

        self._clear_events()

        response = self._request_test_document_change_type_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_document.refresh_from_db()
        self.assertEqual(
            self.test_document.document_type,
            self.test_document_type_2
        )

        events = self._get_test_events()
        # Only the change event, should not have an event for the first
        # .save() method call.
        self.assertEqual(events.count(), 1)
        self.assertEqual(events[0].action_object, self.test_document_type_2)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_document_type_changed.id)

    def test_document_detail_api_view_no_permission(self):
        self._upload_test_document()

        self._clear_events()

        response = self._request_test_document_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_detail_api_view_with_access(self):
        self._upload_test_document()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_document_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data['id'], self.test_document.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_edit_via_patch_api_view_no_permission(self):
        self._upload_test_document()

        document_description = self.test_document.description

        self._clear_events()

        response = self._request_test_document_edit_via_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document.refresh_from_db()
        self.assertEqual(
            self.test_document.description, document_description
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_edit_via_patch_api_view_with_access(self):
        self._upload_test_document()

        document_description = self.test_document.description

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_properties_edit
        )

        self._clear_events()

        response = self._request_test_document_edit_via_patch_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_document.refresh_from_db()
        self.assertNotEqual(
            self.test_document.description, document_description
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)
        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_document_edited.id)

    def test_document_edit_via_put_api_view_no_permission(self):
        self._upload_test_document()

        document_description = self.test_document.description

        self._clear_events()

        response = self._request_test_document_edit_via_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document.refresh_from_db()
        self.assertEqual(
            self.test_document.description, document_description
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_edit_via_put_api_view_with_access(self):
        self._upload_test_document()

        document_description = self.test_document.description

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_properties_edit
        )

        self._clear_events()

        response = self._request_test_document_edit_via_put_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_document.refresh_from_db()
        self.assertNotEqual(
            self.test_document.description, document_description
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)
        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_document_edited.id)

    def test_document_list_api_view_no_permission(self):
        self._upload_test_document()

        self._clear_events()

        response = self._request_test_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_list_api_view_with_access(self):
        self._upload_test_document()

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data['results'][0]['id'], self.test_document.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_upload_api_view_no_permission(self):
        document_count = Document.objects.count()

        self._clear_events()

        response = self._request_test_document_upload_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            Document.objects.count(), document_count
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_upload_api_view_with_access(self):
        self.grant_access(
            obj=self.test_document_type, permission=permission_document_create
        )

        document_count = Document.objects.count()

        self._clear_events()

        response = self._request_test_document_upload_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            Document.objects.count(), document_count + 1
        )

        self.assertEqual(self.test_document.pk, response.data['id'])
        self.assertEqual(
            self.test_document.label, self.test_document.file_latest.filename
        )
        self.assertEqual(self.test_document.pages.count(), 1)

        self.assertEqual(self.test_document.files.count(), 1)
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

        events = self._get_test_events()
        self.assertEqual(events.count(), 5)

        # Document created

        self.assertEqual(events[0].action_object, self.test_document_type)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_document_created.id)

        # Document file created

        self.assertEqual(events[1].action_object, self.test_document)
        self.assertEqual(events[1].actor, self._test_case_user)
        self.assertEqual(events[1].target, self.test_document.file_latest)
        self.assertEqual(events[1].verb, event_document_file_created.id)

        # Document file edited (MIME type, page count update)

        self.assertEqual(events[2].action_object, self.test_document)
        self.assertEqual(events[2].actor, self._test_case_user)
        self.assertEqual(events[2].target, self.test_document.file_latest)
        self.assertEqual(events[2].verb, event_document_file_edited.id)

        # Document version created

        self.assertEqual(events[3].action_object, self.test_document)
        self.assertEqual(events[3].actor, self._test_case_user)
        self.assertEqual(events[3].target, self.test_document.version_active)
        self.assertEqual(events[3].verb, event_document_version_created.id)

        # Document version page created

        self.assertEqual(
            events[4].actor, self._test_case_user
        )
        self.assertEqual(
            events[4].action_object, self.test_document.version_active
        )
        self.assertEqual(
            events[4].target, self.test_document.version_active.pages.first()
        )
        self.assertEqual(
            events[4].verb, event_document_version_page_created.id
        )
