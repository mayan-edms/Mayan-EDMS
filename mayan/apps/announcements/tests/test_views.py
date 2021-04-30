from mayan.apps.testing.tests.base import GenericViewTestCase

from .mixins import AnnouncementTestMixin, AnnouncementViewTestMixin

from ..events import event_announcement_created, event_announcement_edited
from ..models import Announcement
from ..permissions import (
    permission_announcement_create, permission_announcement_delete,
    permission_announcement_edit, permission_announcement_view,
)


class AnnouncementViewTestCase(
    AnnouncementTestMixin, AnnouncementViewTestMixin, GenericViewTestCase
):
    def test_announcement_create_view_no_permission(self):
        announcement_count = Announcement.objects.count()

        self._clear_events()

        response = self._request_test_announcement_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(Announcement.objects.count(), announcement_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_announcement_create_view_with_permissions(self):
        self.grant_permission(permission=permission_announcement_create)

        announcement_count = Announcement.objects.count()

        self._clear_events()

        response = self._request_test_announcement_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Announcement.objects.count(), announcement_count + 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_announcement)
        self.assertEqual(events[0].verb, event_announcement_created.id)

    def test_announcement_delete_view_no_permission(self):
        self._create_test_announcement()

        announcement_count = Announcement.objects.count()

        self._clear_events()

        response = self._request_test_announcement_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Announcement.objects.count(), announcement_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_announcement_delete_view_with_access(self):
        self._create_test_announcement()

        self.grant_access(
            obj=self.test_announcement, permission=permission_announcement_delete
        )

        announcement_count = Announcement.objects.count()

        self._clear_events()

        response = self._request_test_announcement_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Announcement.objects.count(), announcement_count - 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_announcement_edit_view_no_permission(self):
        self._create_test_announcement()

        announcement_label = self.test_announcement.label

        self._clear_events()

        response = self._request_test_announcement_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_announcement.refresh_from_db()
        self.assertEqual(self.test_announcement.label, announcement_label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_announcement_edit_view_with_access(self):
        self._create_test_announcement()

        self.grant_access(
            obj=self.test_announcement, permission=permission_announcement_edit
        )

        announcement_label = self.test_announcement.label

        self._clear_events()

        response = self._request_test_announcement_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_announcement.refresh_from_db()
        self.assertNotEqual(self.test_announcement.label, announcement_label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_announcement)
        self.assertEqual(events[0].verb, event_announcement_edited.id)

    def test_announcement_list_view_with_no_permission(self):
        self._create_test_announcement()

        self._clear_events()

        response = self._request_test_announcement_list_view()
        self.assertNotContains(
            response=response, text=self.test_announcement.label, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_announcement_list_view_with_access(self):
        self._create_test_announcement()

        self.grant_access(
            obj=self.test_announcement, permission=permission_announcement_view
        )

        self._clear_events()

        response = self._request_test_announcement_list_view()
        self.assertContains(
            response=response, text=self.test_announcement.label, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
