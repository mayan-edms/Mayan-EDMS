from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..models import Message
from ..permissions import (
    permission_message_create, permission_message_delete,
    permission_message_edit, permission_message_view
)

from .literals import (
    TEST_LABEL, TEST_LABEL_EDITED, TEST_MESSAGE, TEST_MESSAGE_EDITED
)
from .mixins import MessageAPIViewTestMixin, MessageTestMixin


class MessageAPIViewTestCase(
    MessageAPIViewTestMixin, MessageTestMixin, BaseAPITestCase
):
    def test_message_create_view_no_permission(self):
        response = self._request_message_create_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(Message.objects.count(), 0)

    def test_message_create_view_with_permission(self):
        self.grant_permission(permission=permission_message_create)

        response = self._request_message_create_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        message = Message.objects.first()
        self.assertEqual(response.data['id'], message.pk)
        self.assertEqual(response.data['label'], TEST_LABEL)
        self.assertEqual(response.data['message'], TEST_MESSAGE)

        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(message.label, TEST_LABEL)
        self.assertEqual(message.message, TEST_MESSAGE)

    def test_message_delete_view_no_permission(self):
        self._create_test_message()

        response = self._request_message_delete_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Message.objects.count(), 1)

    def test_message_delete_view_with_access(self):
        self._create_test_message()
        self.grant_access(
            obj=self.test_message, permission=permission_message_delete
        )

        response = self._request_message_delete_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Message.objects.count(), 0)

    def test_message_detail_view_no_permission(self):
        self._create_test_message()

        response = self._request_message_detail_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_message_detail_view_with_access(self):
        self._create_test_message()
        self.grant_access(
            obj=self.test_message, permission=permission_message_view
        )

        response = self._request_message_detail_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['label'], TEST_LABEL)

    def test_message_edit_via_patch_view_no_permission(self):
        self._create_test_message()

        response = self._request_message_edit_via_patch_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_message.refresh_from_db()

        self.assertEqual(self.test_message.label, TEST_LABEL)
        self.assertEqual(self.test_message.message, TEST_MESSAGE)

    def test_message_edit_via_patch_view_with_access(self):
        self._create_test_message()
        self.grant_access(
            obj=self.test_message, permission=permission_message_edit
        )

        response = self._request_message_edit_via_patch_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_message.refresh_from_db()
        self.assertEqual(self.test_message.label, TEST_LABEL_EDITED)
        self.assertEqual(self.test_message.message, TEST_MESSAGE_EDITED)

    def test_message_edit_via_put_view_no_permission(self):
        self._create_test_message()

        response = self._request_message_edit_via_put_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_message.refresh_from_db()

        self.assertEqual(self.test_message.label, TEST_LABEL)
        self.assertEqual(self.test_message.message, TEST_MESSAGE)

    def test_message_edit_via_put_view_with_access(self):
        self._create_test_message()
        self.grant_access(
            obj=self.test_message, permission=permission_message_edit
        )

        response = self._request_message_edit_via_put_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_message.refresh_from_db()
        self.assertEqual(self.test_message.label, TEST_LABEL_EDITED)
        self.assertEqual(self.test_message.message, TEST_MESSAGE_EDITED)
