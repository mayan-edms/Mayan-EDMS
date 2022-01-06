from io import StringIO

from django.contrib.auth import get_user_model
from django.core import management

from mayan.apps.testing.tests.base import BaseTestCase
from mayan.apps.testing.tests.utils import mute_stdout

from ..events import event_otp_disabled
from ..models import UserOTPData

from .mixins import AuthenticationOTPTestMixin


class AuthenticationOTPDisableManagementCommandTestCase(
    AuthenticationOTPTestMixin, BaseTestCase
):
    create_test_case_superuser = True

    def _call_command(self):
        with mute_stdout():
            management.call_command(
                'authentication_otp_disable',
                self._test_case_superuser.username
            )

    def test_command(self):
        self._enable_test_otp()

        self._clear_events()

        self._call_command()

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_superuser)
        self.assertEqual(events[0].target, self._test_case_superuser)
        self.assertEqual(events[0].verb, event_otp_disabled.id)


class AuthenticationOTPInitializeManagementCommandTestCase(
    AuthenticationOTPTestMixin, BaseTestCase
):
    create_test_case_superuser = True

    def _call_command(self):
        with mute_stdout():
            management.call_command(
                'authentication_otp_initialize'
            )

    def test_command(self):
        test_user_count = get_user_model().objects.count()

        UserOTPData.objects.all().delete()

        self._clear_events()

        self._call_command()

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

        self.assertEqual(
            UserOTPData.objects.count(), test_user_count
        )


class AuthenticationOTPStatusManagementCommandTestCase(
    AuthenticationOTPTestMixin, BaseTestCase
):
    create_test_case_superuser = True

    def _call_command(self):
        output = StringIO()
        options = {
            'stdout': output
        }

        management.call_command(
            'authentication_otp_status', self._test_case_superuser.username,
            **options
        )
        output.seek(0)

        return output.getvalue()

    def test_command_with_otp_disabled(self):
        self._clear_events()

        output = self._call_command()
        self.assertTrue('disabled' in output)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_command_with_otp_enabled(self):
        self._enable_test_otp()

        self._clear_events()

        output = self._call_command()
        self.assertTrue('enabled' in output)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
