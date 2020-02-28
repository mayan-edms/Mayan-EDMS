from __future__ import unicode_literals

from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..models import Message
from ..permissions import (
    permission_message_create, permission_message_delete,
    permission_message_edit, permission_message_view
)

from .literals import TEST_LABEL, TEST_MESSAGE
from .mixins import MessageAPITestMixin, MessageTestMixin


class MOTDAPITestCase(MessageAPITestMixin, MessageTestMixin, BaseAPITestCase):
    def test_message_create_api_view_no_permission(self):
        message_count = Message.objects.count()

        response = self._request_test_message_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(Message.objects.count(), message_count)

    def test_message_create_api_view_with_permission(self):
        self.grant_permission(permission=permission_message_create)
        message_count = Message.objects.count()

        response = self._request_test_message_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        message = Message.objects.first()
        self.assertEqual(response.data['id'], message.pk)
        self.assertEqual(response.data['label'], TEST_LABEL)
        self.assertEqual(response.data['message'], TEST_MESSAGE)

        self.assertEqual(Message.objects.count(), message_count + 1)
        self.assertEqual(message.label, TEST_LABEL)
        self.assertEqual(message.message, TEST_MESSAGE)

    def test_message_destroy_api_view_no_permission(self):
        self._create_test_message()
        message_count = Message.objects.count()

        response = self._request_test_message_destroy_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Message.objects.count(), message_count)

    def test_message_destroy_api_view_with_access(self):
        self._create_test_message()
        self.grant_access(
            obj=self.test_message, permission=permission_message_delete
        )
        message_count = Message.objects.count()

        response = self._request_test_message_destroy_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Message.objects.count(), message_count - 1)

    def test_message_partial_update_api_view_no_permission(self):
        self._create_test_message()
        message_values = self._model_instance_to_dictionary(
            instance=self.test_message
        )

        response = self._request_test_message_partial_update_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_message.refresh_from_db()
        self.assertEqual(
            self._model_instance_to_dictionary(
                instance=self.test_message
            ), message_values
        )

    def test_message_partial_update_api_view_with_access(self):
        self._create_test_message()
        self.grant_access(
            obj=self.test_message, permission=permission_message_edit
        )
        message_values = self._model_instance_to_dictionary(
            instance=self.test_message
        )

        response = self._request_test_message_partial_update_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_message.refresh_from_db()
        self.assertNotEqual(
            self._model_instance_to_dictionary(
                instance=self.test_message
            ), message_values
        )

    def test_message_list_api_view_no_permission(self):
        self._create_test_message()
        response = self._request_test_message_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_message_list_api_view_with_access(self):
        self._create_test_message()
        self.grant_access(
            obj=self.test_message, permission=permission_message_view
        )

        response = self._request_test_message_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['label'],
            self.test_message.label
        )

    def test_message_retrive_api_view_no_permission(self):
        self._create_test_message()

        response = self._request_test_message_retrieve_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_message_retrive_view_api_with_access(self):
        self._create_test_message()
        self.grant_access(
            obj=self.test_message, permission=permission_message_view
        )

        response = self._request_test_message_retrieve_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['label'], self.test_message.label)

    def test_message_update_api_view_no_permission(self):
        self._create_test_message()
        message_values = self._model_instance_to_dictionary(
            instance=self.test_message
        )
        response = self._request_test_message_update_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_message.refresh_from_db()
        self.assertEqual(
            self._model_instance_to_dictionary(
                instance=self.test_message
            ), message_values
        )

    def test_message_update_api_view_with_access(self):
        self._create_test_message()
        self.grant_access(
            obj=self.test_message, permission=permission_message_edit
        )
        message_values = self._model_instance_to_dictionary(
            instance=self.test_message
        )

        response = self._request_test_message_update_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_message.refresh_from_db()
        self.assertNotEqual(
            self._model_instance_to_dictionary(
                instance=self.test_message
            ), message_values
        )
