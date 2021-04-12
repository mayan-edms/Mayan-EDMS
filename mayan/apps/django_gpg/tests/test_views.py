from mayan.apps.testing.tests.base import GenericViewTestCase

from ..events import event_key_created, event_key_downloaded
from ..models import Key
from ..permissions import (
    permission_key_delete, permission_key_download, permission_key_upload
)

from .literals import TEST_KEY_PRIVATE_FINGERPRINT
from .mixins import KeyTestMixin, KeyViewTestMixin


class KeyViewTestCase(KeyTestMixin, KeyViewTestMixin, GenericViewTestCase):
    def test_key_delete_view_no_permission(self):
        self._create_test_key_private()

        test_key_count = Key.objects.count()

        self._clear_events()

        response = self._request_test_key_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Key.objects.count(), test_key_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_key_delete_view_with_access(self):
        self._create_test_key_private()

        test_key_count = Key.objects.count()

        self.grant_access(
            obj=self.test_key_private, permission=permission_key_delete
        )

        self._clear_events()

        response = self._request_test_key_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Key.objects.count(), test_key_count - 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_key_download_view_no_permission(self):
        self._create_test_key_private()

        self._clear_events()

        response = self._request_test_key_download_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_key_download_view_with_access(self):
        self.expected_content_types = ('text/html; charset=utf-8',)

        self._create_test_key_private()

        self.grant_access(
            obj=self.test_key_private, permission=permission_key_download
        )

        self._clear_events()

        response = self._request_test_key_download_view()
        self.assert_download_response(
            response=response, content=self.test_key_private.key_data,
            filename=self.test_key_private.key_id,
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_key_private)
        self.assertEqual(events[0].verb, event_key_downloaded.id)

    def test_key_upload_view_no_permission(self):
        self._clear_events()

        response = self._request_test_key_upload_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(Key.objects.count(), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_key_upload_view_with_permission(self):
        self.grant_permission(permission=permission_key_upload)

        self._clear_events()

        response = self._request_test_key_upload_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Key.objects.count(), 1)
        self.assertEqual(
            Key.objects.first().fingerprint, TEST_KEY_PRIVATE_FINGERPRINT
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_key_private)
        self.assertEqual(events[0].verb, event_key_created.id)
