from mayan.apps.testing.tests.base import BaseTestCase

from ..events import event_otp_disabled, event_otp_enabled

from .mixins import AuthenticationOTPTestMixin


class UserOTPDataTestCase(AuthenticationOTPTestMixin, BaseTestCase):
    create_test_case_superuser = True

    def test_method_get_absolute_url(self):
        self._test_case_superuser.otp_data.get_absolute_url()

    def test_otp_disable(self):
        self._enable_test_otp()

        self._clear_events()

        self._test_case_superuser.otp_data.disable()

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_superuser)
        self.assertEqual(events[0].target, self._test_case_superuser)
        self.assertEqual(events[0].verb, event_otp_disabled.id)

    def test_otp_enable(self):
        self._clear_events()

        self._enable_test_otp()

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_superuser)
        self.assertEqual(events[0].target, self._test_case_superuser)
        self.assertEqual(events[0].verb, event_otp_enabled.id)
