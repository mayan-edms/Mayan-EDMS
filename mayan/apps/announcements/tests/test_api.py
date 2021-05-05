from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import event_announcement_created, event_announcement_edited
from ..models import Announcement
from ..permissions import (
    permission_announcement_create, permission_announcement_delete,
    permission_announcement_edit, permission_announcement_view
)

from .literals import TEST_ANNOUNCEMENT_LABEL, TEST_ANNOUNCEMENT_TEXT
from .mixins import AnnouncementAPIViewTestMixin, AnnouncementTestMixin


class AnnouncementAPIViewTestCase(
    AnnouncementAPIViewTestMixin, AnnouncementTestMixin, BaseAPITestCase
):
    def test_announcement_create_api_view_no_permission(self):
        self._clear_events()

        response = self._request_announcement_create_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(Announcement.objects.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_announcement_create_api_view_with_permission(self):
        self.grant_permission(permission=permission_announcement_create)

        self._clear_events()

        response = self._request_announcement_create_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        announcement = Announcement.objects.first()
        self.assertEqual(response.data['id'], announcement.pk)
        self.assertEqual(response.data['label'], TEST_ANNOUNCEMENT_LABEL)
        self.assertEqual(response.data['text'], TEST_ANNOUNCEMENT_TEXT)

        self.assertEqual(Announcement.objects.count(), 1)
        self.assertEqual(announcement.label, TEST_ANNOUNCEMENT_LABEL)
        self.assertEqual(announcement.text, TEST_ANNOUNCEMENT_TEXT)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_announcement)
        self.assertEqual(events[0].verb, event_announcement_created.id)

    def test_announcement_delete_api_view_no_permission(self):
        self._create_test_announcement()

        self._clear_events()

        response = self._request_announcement_delete_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Announcement.objects.count(), 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_announcement_delete_api_view_with_access(self):
        self._create_test_announcement()
        self.grant_access(
            obj=self.test_announcement,
            permission=permission_announcement_delete
        )

        self._clear_events()

        response = self._request_announcement_delete_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Announcement.objects.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_announcement_detail_api_view_no_permission(self):
        self._create_test_announcement()

        self._clear_events()

        response = self._request_announcement_detail_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_announcement_detail_api_view_with_access(self):
        self._create_test_announcement()
        self.grant_access(
            obj=self.test_announcement,
            permission=permission_announcement_view
        )

        self._clear_events()

        response = self._request_announcement_detail_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['label'], self.test_announcement.label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_announcement_edit_api_view_via_patch_view_no_permission(self):
        self._create_test_announcement()

        test_announcement_label = self.test_announcement.label
        test_announcement_text = self.test_announcement.text

        self._clear_events()

        response = self._request_announcement_edit_via_patch_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_announcement.refresh_from_db()
        self.assertEqual(
            self.test_announcement.label, test_announcement_label
        )
        self.assertEqual(self.test_announcement.text, test_announcement_text)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_announcement_edit_api_view_via_patch_view_with_access(self):
        self._create_test_announcement()
        self.grant_access(
            obj=self.test_announcement, permission=permission_announcement_edit
        )

        test_announcement_label = self.test_announcement.label
        test_announcement_text = self.test_announcement.text

        self._clear_events()

        response = self._request_announcement_edit_via_patch_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_announcement.refresh_from_db()
        self.assertNotEqual(
            self.test_announcement.label, test_announcement_label
        )
        self.assertNotEqual(self.test_announcement.text, test_announcement_text)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_announcement)
        self.assertEqual(events[0].verb, event_announcement_edited.id)

    def test_announcement_edit_api_view_via_put_view_no_permission(self):
        self._create_test_announcement()

        test_announcement_label = self.test_announcement.label
        test_announcement_text = self.test_announcement.text

        self._clear_events()

        response = self._request_announcement_edit_via_put_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_announcement.refresh_from_db()
        self.assertEqual(
            self.test_announcement.label, test_announcement_label
        )
        self.assertEqual(self.test_announcement.text, test_announcement_text)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_announcement_edit_api_view_via_put_view_with_access(self):
        self._create_test_announcement()
        self.grant_access(
            obj=self.test_announcement, permission=permission_announcement_edit
        )

        test_announcement_label = self.test_announcement.label
        test_announcement_text = self.test_announcement.text

        self._clear_events()

        response = self._request_announcement_edit_via_put_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_announcement.refresh_from_db()
        self.test_announcement.refresh_from_db()
        self.assertNotEqual(
            self.test_announcement.label, test_announcement_label
        )
        self.assertNotEqual(self.test_announcement.text, test_announcement_text)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_announcement)
        self.assertEqual(events[0].verb, event_announcement_edited.id)
