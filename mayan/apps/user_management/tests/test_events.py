from actstream.models import Action

from mayan.apps.testing.tests.base import GenericViewTestCase


from ..events import event_user_logged_in, event_user_logged_out


class UserEventsTestCase(GenericViewTestCase):
    auto_login_user = False
    create_test_case_user = False

    def test_user_logged_in_event_from_view(self):
        self._create_test_user()

        Action.objects.all().delete()

        result = self.login(
            username=self.test_user.username,
            password=self.test_user.cleartext_password
        )
        self.assertTrue(result)

        action = Action.objects.order_by('timestamp').last()
        self.assertEqual(action.actor, self.test_user)
        self.assertEqual(action.target, self.test_user)
        self.assertEqual(action.verb, event_user_logged_in.id)

    def test_user_logged_out_event_from_view(self):
        self._create_test_user()

        result = self.login(
            username=self.test_user.username,
            password=self.test_user.cleartext_password
        )
        self.assertTrue(result)

        Action.objects.all().delete()

        self.logout()

        action = Action.objects.order_by('timestamp').last()
        self.assertEqual(action.actor, self.test_user)
        self.assertEqual(action.target, self.test_user)
        self.assertEqual(action.verb, event_user_logged_out.id)
