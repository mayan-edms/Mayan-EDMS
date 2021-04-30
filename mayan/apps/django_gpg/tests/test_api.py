from rest_framework import status

from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..events import event_key_created
from ..models import Key
from ..permissions import (
    permission_key_delete, permission_key_upload, permission_key_view
)

from .literals import TEST_KEY_PRIVATE_FINGERPRINT
from .mixins import KeyAPIViewTestMixin, KeyTestMixin


class KeyAPITestCase(KeyTestMixin, KeyAPIViewTestMixin, BaseAPITestCase):
    def test_key_create_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_key_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(Key.objects.all().count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_key_create_api_view_with_permission(self):
        self.grant_permission(permission=permission_key_upload)

        self._clear_events()

        response = self._request_test_key_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data['fingerprint'], TEST_KEY_PRIVATE_FINGERPRINT
        )

        key = Key.objects.first()
        self.assertEqual(Key.objects.count(), 1)
        self.assertEqual(key.fingerprint, TEST_KEY_PRIVATE_FINGERPRINT)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_key_private)
        self.assertEqual(events[0].verb, event_key_created.id)

    def test_key_delete_api_view_no_permission(self):
        self._create_test_key_private()

        self._clear_events()

        response = self._request_test_key_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(Key.objects.count(), 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_key_delete_api_view_with_access(self):
        self._create_test_key_private()
        self.grant_access(
            obj=self.test_key_private, permission=permission_key_delete
        )

        self._clear_events()

        response = self._request_test_key_delete_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Key.objects.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_key_detail_api_view_no_permission(self):
        self._create_test_key_private()

        self._clear_events()

        response = self._request_test_key_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_key_detail_api_view_with_access(self):
        self._create_test_key_private()
        self.grant_access(
            obj=self.test_key_private, permission=permission_key_view
        )

        self._clear_events()

        response = self._request_test_key_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['fingerprint'], self.test_key_private.fingerprint
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
