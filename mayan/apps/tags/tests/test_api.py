from django.utils.encoding import force_text

from rest_framework import status

from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import (
    event_tag_attached, event_tag_created, event_tag_edited, event_tag_removed
)
from ..models import Tag
from ..permissions import (
    permission_tag_attach, permission_tag_create, permission_tag_delete,
    permission_tag_edit, permission_tag_remove, permission_tag_view
)

from .mixins import TagAPIViewTestMixin, TagTestMixin


class TagAPIViewTestCase(TagAPIViewTestMixin, TagTestMixin, BaseAPITestCase):
    def test_tag_create_api_view_no_permission(self):
        tag_count = Tag.objects.count()

        self._clear_events()

        response = self._request_test_tag_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(Tag.objects.count(), tag_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_tag_create_api_view_with_permission(self):
        self.grant_permission(permission=permission_tag_create)

        tag_count = Tag.objects.count()

        self._clear_events()

        response = self._request_test_tag_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Tag.objects.count(), tag_count + 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_tag)
        self.assertEqual(events[0].verb, event_tag_created.id)

    def test_tag_delete_api_view_no_permission(self):
        self._create_test_tag()

        tag_count = Tag.objects.count()

        self._clear_events()

        response = self._request_test_tag_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Tag.objects.count(), tag_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_tag_delete_api_view_with_access(self):
        self._create_test_tag()

        self.grant_access(obj=self.test_tag, permission=permission_tag_delete)

        tag_count = Tag.objects.count()

        self._clear_events()

        response = self._request_test_tag_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Tag.objects.count(), tag_count - 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_tag_detail_api_view_no_permission(self):
        self._create_test_tag()

        self._clear_events()

        response = self._request_test_tag_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_tag_detail_api_view_with_access(self):
        self._create_test_tag()
        self.grant_access(
            obj=self.test_tag, permission=permission_tag_view
        )

        self._clear_events()

        response = self._request_test_tag_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['label'], self.test_tag.label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_tag_edit_api_view_via_patch_no_permission(self):
        self._create_test_tag()

        tag_label = self.test_tag.label
        tag_color = self.test_tag.color

        self._clear_events()

        response = self._request_test_tag_edit_api_view(verb='patch')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_tag.refresh_from_db()
        self.assertEqual(self.test_tag.label, tag_label)
        self.assertEqual(self.test_tag.color, tag_color)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_tag_edit_api_view_via_patch_with_access(self):
        self._create_test_tag()

        self.grant_access(obj=self.test_tag, permission=permission_tag_edit)

        tag_label = self.test_tag.label
        tag_color = self.test_tag.color

        self._clear_events()

        response = self._request_test_tag_edit_api_view(verb='patch')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_tag.refresh_from_db()
        self.assertNotEqual(self.test_tag.label, tag_label)
        self.assertNotEqual(self.test_tag.color, tag_color)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_tag)
        self.assertEqual(events[0].verb, event_tag_edited.id)

    def test_tag_edit_api_view_via_put_no_permission(self):
        self._create_test_tag()

        tag_label = self.test_tag.label
        tag_color = self.test_tag.color

        self._clear_events()

        response = self._request_test_tag_edit_api_view(verb='put')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_tag.refresh_from_db()
        self.assertEqual(self.test_tag.label, tag_label)
        self.assertEqual(self.test_tag.color, tag_color)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_tag_edit_api_view_via_put_with_access(self):
        self._create_test_tag()

        self.grant_access(obj=self.test_tag, permission=permission_tag_edit)

        tag_label = self.test_tag.label
        tag_color = self.test_tag.color

        self._clear_events()

        response = self._request_test_tag_edit_api_view(verb='put')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_tag.refresh_from_db()
        self.assertNotEqual(self.test_tag.label, tag_label)
        self.assertNotEqual(self.test_tag.color, tag_color)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_tag)
        self.assertEqual(events[0].verb, event_tag_edited.id)

    def test_tag_list_api_view_no_permission(self):
        self._create_test_tag()

        self._clear_events()

        response = self._request_test_tag_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_tag_list_api_view_with_access(self):
        self._create_test_tag()
        self.grant_access(
            obj=self.test_tag, permission=permission_tag_view
        )

        self._clear_events()

        response = self._request_test_tag_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['label'],
            self.test_tag.label
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class TagDocumentAPIViewTestCase(
    DocumentTestMixin, TagAPIViewTestMixin, TagTestMixin, BaseAPITestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_tag()
        self._create_test_document_stub()

    def test_tag_document_list_api_view_no_permission(self):
        self.test_tag.documents.add(self.test_document)

        self._clear_events()

        response = self._request_test_tag_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_tag_document_list_api_view_with_tag_access(self):
        self.test_tag.documents.add(self.test_document)

        self.grant_access(obj=self.test_tag, permission=permission_tag_view)

        self._clear_events()

        response = self._request_test_tag_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_tag_document_list_api_view_with_document_access(self):
        self.test_tag.documents.add(self.test_document)

        self._clear_events()

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_tag_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_tag_document_list_api_view_with_full_access(self):
        self.test_tag.documents.add(self.test_document)

        self.grant_access(obj=self.test_tag, permission=permission_tag_view)
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_tag_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data['results'][0]['uuid'],
            force_text(s=self.test_document.uuid)
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_tag_trashed_document_list_api_view_with_full_access(self):
        self.test_tag.documents.add(self.test_document)

        self.grant_access(obj=self.test_tag, permission=permission_tag_view)
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_tag_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


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

        self.assertTrue(self.test_tag not in self.test_document.tags.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_attach_tag_api_view_with_document_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_tag_attach
        )

        self._clear_events()

        response = self._request_test_document_tag_attach_api_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertTrue(self.test_tag not in self.test_document.tags.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_attach_tag_api_view_with_tag_access(self):
        self.grant_access(
            obj=self.test_tag, permission=permission_tag_attach
        )

        self._clear_events()

        response = self._request_test_document_tag_attach_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(self.test_tag not in self.test_document.tags.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_attach_tag_api_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_tag_attach
        )
        self.grant_access(
            obj=self.test_tag, permission=permission_tag_attach
        )

        self._clear_events()

        response = self._request_test_document_tag_attach_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(self.test_tag in self.test_document.tags.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_tag)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_tag_attached.id)

    def test_trashed_document_attach_tag_api_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_tag_attach
        )
        self.grant_access(
            obj=self.test_tag, permission=permission_tag_attach
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_tag_attach_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(self.test_tag not in self.test_document.tags.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_tag_list_api_view_no_permission(self):
        self.test_tag.documents.add(self.test_document)

        self._clear_events()

        response = self._request_test_document_tag_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_tag_list_api_view_with_document_access(self):
        self.test_tag.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_document, permission=permission_tag_view
        )

        self._clear_events()

        response = self._request_test_document_tag_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_tag_list_api_view_with_tag_access(self):
        self.test_tag.documents.add(self.test_document)

        self.grant_access(obj=self.test_tag, permission=permission_tag_view)

        self._clear_events()

        response = self._request_test_document_tag_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_tag_list_api_view_with_full_access(self):
        self.test_tag.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_document, permission=permission_tag_view
        )
        self.grant_access(obj=self.test_tag, permission=permission_tag_view)

        self._clear_events()

        response = self._request_test_document_tag_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['label'], self.test_tag.label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_tag_list_api_view_with_full_access(self):
        self.test_tag.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_document, permission=permission_tag_view
        )
        self.grant_access(obj=self.test_tag, permission=permission_tag_view)

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_tag_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_tag_remove_api_view_no_permission(self):
        self.test_tag.documents.add(self.test_document)

        self._clear_events()

        response = self._request_test_document_tag_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(self.test_tag in self.test_document.tags.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_tag_remove_api_view_with_document_access(self):
        self.test_tag.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_document, permission=permission_tag_remove
        )

        self._clear_events()

        response = self._request_test_document_tag_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertTrue(self.test_tag in self.test_document.tags.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_tag_remove_api_view_with_tag_access(self):
        self.test_tag.documents.add(self.test_document)

        self.grant_access(obj=self.test_tag, permission=permission_tag_remove)

        self._clear_events()

        response = self._request_test_document_tag_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(self.test_tag in self.test_document.tags.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_tag_remove_api_view_with_full_access(self):
        self.test_tag.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_document, permission=permission_tag_remove
        )
        self.grant_access(obj=self.test_tag, permission=permission_tag_remove)

        self._clear_events()

        response = self._request_test_document_tag_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertFalse(self.test_tag in self.test_document.tags.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_tag)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_document)
        self.assertEqual(events[0].verb, event_tag_removed.id)

    def test_trashed_document_tag_remove_api_view_with_full_access(self):
        self.test_tag.documents.add(self.test_document)

        self.grant_access(
            obj=self.test_document, permission=permission_tag_remove
        )
        self.grant_access(obj=self.test_tag, permission=permission_tag_remove)

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_tag_remove_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertTrue(self.test_tag in self.test_document.tags.all())

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
