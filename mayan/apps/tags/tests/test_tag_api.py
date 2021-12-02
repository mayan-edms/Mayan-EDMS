from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import event_tag_created, event_tag_edited
from ..models import Tag
from ..permissions import (
    permission_tag_create, permission_tag_delete, permission_tag_edit,
    permission_tag_view
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
