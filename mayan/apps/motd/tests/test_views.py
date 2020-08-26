from mayan.apps.events.tests.mixins import EventTestCaseMixin
from mayan.apps.testing.tests.base import GenericViewTestCase

from .mixins import MessageTestMixin, MessageViewTestMixin

from ..events import event_message_created, event_message_edited
from ..models import Message
from ..permissions import (
    permission_message_create, permission_message_delete,
    permission_message_edit, permission_message_view,
)


class MessageViewTestCase(
    MessageTestMixin, MessageViewTestMixin, EventTestCaseMixin,
    GenericViewTestCase
):
    _test_event_object_name = 'test_message'

    def test_message_create_view_no_permission(self):
        message_count = Message.objects.count()

        self._clear_events()

        response = self._request_test_message_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(Message.objects.count(), message_count)

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_message_create_view_with_permissions(self):
        self.grant_permission(permission=permission_message_create)

        message_count = Message.objects.count()

        self._clear_events()

        response = self._request_test_message_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Message.objects.count(), message_count + 1)

        event = self._get_test_object_event()
        self.assertEqual(event.verb, event_message_created.id)
        self.assertEqual(event.actor, self._test_case_user)

    def test_message_delete_view_no_permission(self):
        self._create_test_message()

        message_count = Message.objects.count()

        self._clear_events()

        response = self._request_test_message_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Message.objects.count(), message_count)

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_message_delete_view_with_access(self):
        self._create_test_message()

        self.grant_access(
            obj=self.test_message, permission=permission_message_delete
        )

        message_count = Message.objects.count()

        self._clear_events()

        response = self._request_test_message_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Message.objects.count(), message_count - 1)

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_message_edit_view_no_permission(self):
        self._create_test_message()

        message_label = self.test_message.label

        self._clear_events()

        response = self._request_test_message_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_message.refresh_from_db()
        self.assertEqual(self.test_message.label, message_label)

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_message_edit_view_with_access(self):
        self._create_test_message()

        self.grant_access(
            obj=self.test_message, permission=permission_message_edit
        )

        message_label = self.test_message.label

        self._clear_events()

        response = self._request_test_message_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_message.refresh_from_db()
        self.assertNotEqual(self.test_message.label, message_label)

        event = self._get_test_object_event()
        self.assertEqual(event.verb, event_message_edited.id)
        self.assertEqual(event.actor, self._test_case_user)

    def test_message_list_view_with_no_permission(self):
        self._create_test_message()

        self._clear_events()

        response = self._request_test_message_list_view()
        self.assertNotContains(
            response=response, text=self.test_message.label, status_code=200
        )

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_message_list_view_with_access(self):
        self._create_test_message()

        self.grant_access(
            obj=self.test_message, permission=permission_message_view
        )

        self._clear_events()

        response = self._request_test_message_list_view()
        self.assertContains(
            response=response, text=self.test_message.label, status_code=200
        )

        event = self._get_test_object_event()
        self.assertEqual(event, None)
