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
    _test_event_object_name = 'test_announcement'

    def test_announcement_create_view_no_permission(self):
        announcement_count = Announcement.objects.count()

        self._clear_events()

        response = self._request_test_announcement_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(Announcement.objects.count(), announcement_count)

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_announcement_create_view_with_permissions(self):
        self.grant_permission(permission=permission_announcement_create)

        announcement_count = Announcement.objects.count()

        self._clear_events()

        response = self._request_test_announcement_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Announcement.objects.count(), announcement_count + 1)

        event = self._get_test_object_event()
        self.assertEqual(event.actor, self._test_case_user)
        self.assertEqual(event.action_object, None)
        self.assertEqual(event.target, self.test_announcement)
        self.assertEqual(event.verb, event_announcement_created.id)

    def test_announcement_delete_view_no_permission(self):
        self._create_test_announcement()

        announcement_count = Announcement.objects.count()

        self._clear_events()

        response = self._request_test_announcement_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Announcement.objects.count(), announcement_count)

        event = self._get_test_object_event()
        self.assertEqual(event, None)

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

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_announcement_edit_view_no_permission(self):
        self._create_test_announcement()

        announcement_label = self.test_announcement.label

        self._clear_events()

        response = self._request_test_announcement_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_announcement.refresh_from_db()
        self.assertEqual(self.test_announcement.label, announcement_label)

        event = self._get_test_object_event()
        self.assertEqual(event, None)

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

        event = self._get_test_object_event()
        self.assertEqual(event.actor, self._test_case_user)
        self.assertEqual(event.action_object, None)
        self.assertEqual(event.target, self.test_announcement)
        self.assertEqual(event.verb, event_announcement_edited.id)

    def test_announcement_list_view_with_no_permission(self):
        self._create_test_announcement()

        self._clear_events()

        response = self._request_test_announcement_list_view()
        self.assertNotContains(
            response=response, text=self.test_announcement.label, status_code=200
        )

        event = self._get_test_object_event()
        self.assertEqual(event, None)

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

        event = self._get_test_object_event()
        self.assertEqual(event, None)
