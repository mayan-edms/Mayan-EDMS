from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import event_message_created, event_message_edited
from ..models import Message
from ..permissions import (
    permission_message_create, permission_message_delete,
    permission_message_edit, permission_message_view
)

from .mixins import MessageAPIViewTestMixin, MessageTestMixin


class MessageAPIViewTestCase(
    MessageAPIViewTestMixin, MessageTestMixin, BaseAPITestCase
):
    def test_message_create_api_view_no_permission(self):
        message_count = Message.objects.count()

        self._clear_events()

        response = self._request_test_message_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(Message.objects.count(), message_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_message_create_api_view_with_permission(self):
        self.grant_permission(permission=permission_message_create)

        message_count = Message.objects.count()

        self._clear_events()

        response = self._request_test_message_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Message.objects.count(), message_count + 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_message)
        self.assertEqual(events[0].verb, event_message_created.id)

    def test_message_create_api_view_for_superuser_with_permission(self):
        self.grant_permission(permission=permission_message_create)

        message_count = Message.objects.count()

        self._create_test_superuser()

        self._clear_events()

        response = self._request_test_message_create_api_view(
            extra_data={'user': self.test_superuser.pk}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(Message.objects.count(), message_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_message_delete_api_view_no_permission(self):
        self._create_test_message()

        message_count = Message.objects.count()

        self._clear_events()

        response = self._request_test_message_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Message.objects.count(), message_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_message_delete_api_view_with_access(self):
        self._create_test_message()

        self.grant_access(
            obj=self.test_message, permission=permission_message_delete
        )

        message_count = Message.objects.count()

        self._clear_events()

        response = self._request_test_message_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Message.objects.count(), message_count - 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_message_detail_api_view_no_permission(self):
        self._create_test_message()

        self._clear_events()

        response = self._request_test_message_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_message_detail_api_view_with_access(self):
        self._create_test_message()
        self.grant_access(
            obj=self.test_message, permission=permission_message_view
        )

        self._clear_events()

        response = self._request_test_message_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['id'], self.test_message.pk)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_message_edit_api_view_via_patch_no_permission(self):
        self._create_test_message()

        message_read = self.test_message.read

        self._clear_events()

        response = self._request_test_message_edit_api_view(verb='patch')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_message.refresh_from_db()
        self.assertEqual(self.test_message.read, message_read)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_message_edit_api_view_via_patch_with_access(self):
        self._create_test_message()

        self.grant_access(
            obj=self.test_message, permission=permission_message_edit
        )

        message_read = self.test_message.read

        self._clear_events()

        response = self._request_test_message_edit_api_view(verb='patch')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_message.refresh_from_db()
        self.assertNotEqual(self.test_message.read, message_read)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_message)
        self.assertEqual(events[0].verb, event_message_edited.id)

    def test_message_edit_api_view_via_put_no_permission(self):
        self._create_test_message()

        message_read = self.test_message.read

        self._clear_events()

        response = self._request_test_message_edit_api_view(verb='put')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_message.refresh_from_db()
        self.assertEqual(self.test_message.read, message_read)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_message_edit_api_view_via_put_with_access(self):
        self._create_test_message()

        self.grant_access(
            obj=self.test_message, permission=permission_message_edit
        )

        message_read = self.test_message.read

        self._clear_events()

        response = self._request_test_message_edit_api_view(verb='put')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_message.refresh_from_db()
        self.assertNotEqual(self.test_message.read, message_read)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_message)
        self.assertEqual(events[0].verb, event_message_edited.id)

    def test_message_list_api_view_no_permission(self):
        self._create_test_message()

        self._clear_events()

        response = self._request_test_message_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_message_list_api_view_with_access(self):
        self._create_test_message()
        self.grant_access(
            obj=self.test_message, permission=permission_message_view
        )

        self._clear_events()

        response = self._request_test_message_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['id'],
            self.test_message.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
