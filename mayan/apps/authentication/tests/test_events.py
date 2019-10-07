from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.views import (
    INTERNAL_RESET_SESSION_TOKEN, INTERNAL_RESET_URL_TOKEN,
)
from django.core import mail

from actstream.models import Action

from mayan.apps.common.tests.base import GenericViewTestCase
from mayan.apps.events.utils import create_system_user

from ..events import (
    event_user_authentication_error, event_user_password_reset_complete,
    event_user_password_reset_started
)


class AuthenticationEventsTestCase(GenericViewTestCase):
    auto_login_user = False

    def setUp(self):
        super(AuthenticationEventsTestCase, self).setUp()
        create_system_user()

    def test_user_authentication_failure_event(self):
        Action.objects.all().delete()
        response = self.post(viewname=settings.LOGIN_URL)
        self.assertEqual(response.status_code, 200)

        action = Action.objects.last()
        self.assertEqual(action.verb, event_user_authentication_error.id)

    def test_user_password_reset_started_event(self):
        Action.objects.all().delete()
        response = self.post(
            viewname='authentication:password_reset_view', data={
                'email': self._test_case_user.email,
            }
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(len(mail.outbox), 1)

        action = Action.objects.last()
        self.assertEqual(action.verb, event_user_password_reset_started.id)

    def test_user_password_reset_complete_event(self):
        response = self.post(
            viewname='authentication:password_reset_view', data={
                'email': self._test_case_user.email,
            }
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(len(mail.outbox), 1)

        email_parts = mail.outbox[0].body.replace('\n', '').split('/')
        uidb64 = email_parts[-3]
        token = email_parts[-2]

        # Add the token to the session
        session = self.client.session
        session[INTERNAL_RESET_SESSION_TOKEN] = token
        session.save()

        Action.objects.all().delete()

        new_password = 'new_password_123'
        response = self.post(
            viewname='authentication:password_reset_confirm_view',
            kwargs={'uidb64': uidb64, 'token': INTERNAL_RESET_URL_TOKEN}, data={
                'new_password1': new_password,
                'new_password2': new_password
            }
        )

        self.assertNotIn(INTERNAL_RESET_SESSION_TOKEN, self.client.session)

        action = Action.objects.last()
        self.assertEqual(action.verb, event_user_password_reset_complete.id)
