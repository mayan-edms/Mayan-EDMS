from mayan.apps.testing.tests.base import GenericViewTestCase
from mayan.apps.user_management.events import event_user_edited

from ..events import event_user_logged_in, event_user_logged_out


class UserEventsTestCase(GenericViewTestCase):
    auto_login_user = False
    create_test_case_user = False

    def test_user_logged_in_event_from_view(self):
        self._create_test_user()

        last_login = self.test_user.last_login

        self._clear_events()

        result = self.login(
            username=self.test_user.username,
            password=self.test_user.cleartext_password
        )
        self.assertTrue(result)

        self.assertEqual(self.test_user.last_login, last_login)
        self.assertEqual(self.test_user.last_login, None)

        events = self._get_test_events()
        self.assertEqual(events.count(), 2)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self.test_user)
        self.assertEqual(events[0].target, self.test_user)
        self.assertEqual(events[0].verb, event_user_edited.id)

        self.assertEqual(events[1].action_object, None)
        self.assertEqual(events[1].actor, self.test_user)
        self.assertEqual(events[1].target, self.test_user)
        self.assertEqual(events[1].verb, event_user_logged_in.id)

    def test_user_logged_out_event_from_view(self):
        self._create_test_user()

        result = self.login(
            username=self.test_user.username,
            password=self.test_user.cleartext_password
        )
        self.assertTrue(result)

        self._clear_events()

        self.logout()

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self.test_user)
        self.assertEqual(events[0].target, self.test_user)
        self.assertEqual(events[0].verb, event_user_logged_out.id)
