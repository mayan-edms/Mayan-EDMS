from mayan.apps.testing.tests.base import GenericViewTestCase

from ..events import event_key_created, event_key_downloaded
from ..models import Key
from ..permissions import permission_key_download, permission_key_upload

from .literals import TEST_KEY_PRIVATE_FINGERPRINT
from .mixins import KeyTestMixin, KeyViewTestMixin


class KeyViewTestCase(KeyTestMixin, KeyViewTestMixin, GenericViewTestCase):
    _test_event_object_name = 'test_key_private'

    def test_key_download_view_no_permission(self):
        self._create_test_key_private()

        self._clear_events()

        response = self._request_test_key_download_view()
        self.assertEqual(response.status_code, 404)

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_key_download_view_with_permission(self):
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

        event = self._get_test_object_event()
        self.assertEqual(event.actor, self._test_case_user)
        self.assertEqual(event.target, self.test_key_private)
        self.assertEqual(event.verb, event_key_downloaded.id)

    def test_key_upload_view_no_permission(self):
        self._clear_events()

        response = self._request_test_key_upload_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(Key.objects.count(), 0)

        event = self._get_test_object_event()
        self.assertEqual(event, None)

    def test_key_upload_view_with_permission(self):
        self.grant_permission(permission=permission_key_upload)

        self._clear_events()

        response = self._request_test_key_upload_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Key.objects.count(), 1)
        self.assertEqual(
            Key.objects.first().fingerprint, TEST_KEY_PRIVATE_FINGERPRINT
        )

        event = self._get_test_object_event()
        self.assertEqual(event.actor, self._test_case_user)
        self.assertEqual(event.target, self.test_key_private)
        self.assertEqual(event.verb, event_key_created.id)
