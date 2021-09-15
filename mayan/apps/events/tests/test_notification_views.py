from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..models import Notification

from .mixins import NotificationTestMixin, NotificationViewTestMixin


class NotificationViewTestCase(
    NotificationTestMixin, NotificationViewTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_event_type()
        self._create_test_user()

        self.test_event_type.commit(
            actor=self.test_user, action_object=self.test_document_type
        )

    def test_notification_list_view(self):
        response = self._request_test_notification_list_view()
        self.assertEqual(response.status_code, 200)

    def test_notification_mark_read_all_view(self):
        self._create_test_notification()
        notification_count = Notification.objects.get_unread().count()

        response = self._request_test_notification_mark_read_all_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            Notification.objects.get_unread().count(),
            notification_count - 1
        )

    def test_notification_mark_read_view(self):
        self._create_test_notification()
        notification_count = Notification.objects.get_unread().count()

        response = self._request_test_notification_mark_read()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            Notification.objects.get_unread().count(),
            notification_count - 1
        )
