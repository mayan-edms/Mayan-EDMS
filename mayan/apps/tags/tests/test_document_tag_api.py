from rest_framework import status

from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import event_tag_attached, event_tag_removed
from ..permissions import (
    permission_tag_attach, permission_tag_remove, permission_tag_view
)

from .mixins import TagAPIViewTestMixin, TagTestMixin


class DocumentTagAPIViewTestCase(
    DocumentTestMixin, TagAPIViewTestMixin, TagTestMixin, BaseAPITestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_tag()
        self._create_test_document_stub()

    def test_document_attach_tag_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_tag_attach_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(self._test_tag not in self._test_document.tags.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_attach_tag_api_view_with_document_access(self):
        self.grant_access(
            obj=self._test_document, permission=permission_tag_attach
        )

        self._clear_events()

        response = self._request_test_document_tag_attach_api_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertTrue(self._test_tag not in self._test_document.tags.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_attach_tag_api_view_with_tag_access(self):
        self.grant_access(
            obj=self._test_tag, permission=permission_tag_attach
        )

        self._clear_events()

        response = self._request_test_document_tag_attach_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(self._test_tag not in self._test_document.tags.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_attach_tag_api_view_with_full_access(self):
        self.grant_access(
            obj=self._test_document, permission=permission_tag_attach
        )
        self.grant_access(
            obj=self._test_tag, permission=permission_tag_attach
        )

        self._clear_events()

        response = self._request_test_document_tag_attach_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(self._test_tag in self._test_document.tags.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self._test_tag)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_document)
        self.assertEqual(events[0].verb, event_tag_attached.id)

    def test_trashed_document_attach_tag_api_view_with_full_access(self):
        self.grant_access(
            obj=self._test_document, permission=permission_tag_attach
        )
        self.grant_access(
            obj=self._test_tag, permission=permission_tag_attach
        )

        self._test_document.delete()

        self._clear_events()

        response = self._request_test_document_tag_attach_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(self._test_tag not in self._test_document.tags.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_tag_list_api_view_no_permission(self):
        self._test_tag.attach_to(document=self._test_document)

        self._clear_events()

        response = self._request_test_document_tag_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_tag_list_api_view_with_document_access(self):
        self._test_tag.attach_to(document=self._test_document)

        self.grant_access(
            obj=self._test_document, permission=permission_tag_view
        )

        self._clear_events()

        response = self._request_test_document_tag_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_tag_list_api_view_with_tag_access(self):
        self._test_tag.attach_to(document=self._test_document)

        self.grant_access(obj=self._test_tag, permission=permission_tag_view)

        self._clear_events()

        response = self._request_test_document_tag_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_tag_list_api_view_with_full_access(self):
        self._test_tag.attach_to(document=self._test_document)

        self.grant_access(
            obj=self._test_document, permission=permission_tag_view
        )
        self.grant_access(obj=self._test_tag, permission=permission_tag_view)

        self._clear_events()

        response = self._request_test_document_tag_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['label'], self._test_tag.label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_tag_list_api_view_with_full_access(self):
        self._test_tag.attach_to(document=self._test_document)

        self.grant_access(
            obj=self._test_document, permission=permission_tag_view
        )
        self.grant_access(obj=self._test_tag, permission=permission_tag_view)

        self._test_document.delete()

        self._clear_events()

        response = self._request_test_document_tag_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_tag_remove_api_view_no_permission(self):
        self._test_tag.attach_to(document=self._test_document)

        self._clear_events()

        response = self._request_test_document_tag_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(self._test_tag in self._test_document.tags.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_tag_remove_api_view_with_document_access(self):
        self._test_tag.attach_to(document=self._test_document)

        self.grant_access(
            obj=self._test_document, permission=permission_tag_remove
        )

        self._clear_events()

        response = self._request_test_document_tag_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertTrue(self._test_tag in self._test_document.tags.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_tag_remove_api_view_with_tag_access(self):
        self._test_tag.attach_to(document=self._test_document)

        self.grant_access(obj=self._test_tag, permission=permission_tag_remove)

        self._clear_events()

        response = self._request_test_document_tag_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(self._test_tag in self._test_document.tags.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_tag_remove_api_view_with_full_access(self):
        self._test_tag.attach_to(document=self._test_document)

        self.grant_access(
            obj=self._test_document, permission=permission_tag_remove
        )
        self.grant_access(obj=self._test_tag, permission=permission_tag_remove)

        self._clear_events()

        response = self._request_test_document_tag_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertFalse(self._test_tag in self._test_document.tags.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self._test_tag)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_document)
        self.assertEqual(events[0].verb, event_tag_removed.id)

    def test_trashed_document_tag_remove_api_view_with_full_access(self):
        self._test_tag.attach_to(document=self._test_document)

        self.grant_access(
            obj=self._test_document, permission=permission_tag_remove
        )
        self.grant_access(obj=self._test_tag, permission=permission_tag_remove)

        self._test_document.delete()

        self._clear_events()

        response = self._request_test_document_tag_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(self._test_tag in self._test_document.tags.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
