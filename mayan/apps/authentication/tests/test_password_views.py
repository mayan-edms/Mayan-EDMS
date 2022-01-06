from django.contrib.auth.views import INTERNAL_RESET_SESSION_TOKEN
from django.core import mail
from django.test import override_settings
from django.urls import reverse

from mayan.apps.common.settings import setting_home_view
from mayan.apps.testing.tests.base import GenericViewTestCase
from mayan.apps.user_management.events import event_user_edited
from mayan.apps.user_management.permissions import permission_user_edit
from mayan.apps.user_management.tests.literals import (
    TEST_USER_PASSWORD_EDITED
)

from .literals import TEST_PASSWORD_NEW
from .mixins import PasswordResetViewTestMixin, UserPasswordViewTestMixin


class CurrentUserViewTestCase(GenericViewTestCase):
    def _request_current_user_password_change_view(self, new_password):
        return self.post(
            viewname='authentication:password_change_view', data={
                'old_password': self._test_case_user.cleartext_password,
                'new_password1': new_password,
                'new_password2': new_password
            }
        )

    def test_current_user_set_password_view(self):
        self._clear_events()

        response = self._request_current_user_password_change_view(
            new_password=TEST_PASSWORD_NEW
        )
        self.assertEqual(response.status_code, 302)

        self._test_case_user.refresh_from_db()
        self.assertTrue(
            self._test_case_user.check_password(
                raw_password=TEST_PASSWORD_NEW
            )
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_case_user)
        self.assertEqual(events[0].verb, event_user_edited.id)


class PasswordResetViewTestCase(
    PasswordResetViewTestMixin, GenericViewTestCase
):
    auto_login_user = False
    create_test_case_superuser = True

    def test_password_reset_view(self):
        self.logout()
        self._clear_events()

        response = self._request_password_reset_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(len(mail.outbox), 1)
        email_parts = mail.outbox[0].body.replace('\n', '').split('/')
        uidb64 = email_parts[-3]
        token = email_parts[-2]

        # Add the token to the session.
        session = self.client.session
        session[INTERNAL_RESET_SESSION_TOKEN] = token
        session.save()

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

        self._clear_events()

        response = self._request_password_reset_confirm_view(
            new_password=TEST_PASSWORD_NEW, uidb64=uidb64
        )
        self.assertNotIn(INTERNAL_RESET_SESSION_TOKEN, self.client.session)

        self._test_case_superuser.refresh_from_db()
        self.assertTrue(
            self._test_case_superuser.check_password(
                raw_password=TEST_PASSWORD_NEW
            )
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_superuser)
        self.assertEqual(events[0].target, self._test_case_superuser)
        self.assertEqual(events[0].verb, event_user_edited.id)

    @override_settings(AUTHENTICATION_DISABLE_PASSWORD_RESET=False)
    def test_password_reset_get_view_with_disable_false(self):
        self.logout()

        self._clear_events()

        response = self._request_password_reset_get_view()

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(mail.outbox), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    @override_settings(AUTHENTICATION_DISABLE_PASSWORD_RESET=True)
    def test_password_reset_get_view_with_disable_true(self):
        self.logout()

        self._clear_events()

        response = self._request_password_reset_get_view()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url, reverse(viewname=setting_home_view.value)
        )

        self.assertEqual(len(mail.outbox), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    @override_settings(AUTHENTICATION_DISABLE_PASSWORD_RESET=False)
    def test_password_reset_post_view_with_disable_false(self):
        self.logout()

        self._clear_events()

        response = self._request_password_reset_post_view()

        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(response.url, setting_home_view.value)

        self.assertEqual(len(mail.outbox), 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    @override_settings(AUTHENTICATION_DISABLE_PASSWORD_RESET=True)
    def test_password_reset_post_view_with_disable_true(self):
        self.logout()

        self._clear_events()

        response = self._request_password_reset_post_view()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url, reverse(viewname=setting_home_view.value)
        )

        self.assertEqual(len(mail.outbox), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class UserPasswordViewTestCase(
    UserPasswordViewTestMixin, GenericViewTestCase
):
    def test_user_set_password_view_no_permission(self):
        self._create_test_user()

        password_hash = self.test_user.password

        self._clear_events()

        response = self._request_test_user_password_set_view(
            password=TEST_USER_PASSWORD_EDITED
        )
        self.assertEqual(response.status_code, 404)

        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.password, password_hash)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_set_password_view_with_access(self):
        self._create_test_user()
        self.grant_access(obj=self.test_user, permission=permission_user_edit)

        password_hash = self.test_user.password

        self._clear_events()

        response = self._request_test_user_password_set_view(
            password=TEST_USER_PASSWORD_EDITED
        )
        self.assertEqual(response.status_code, 302)

        self.test_user.refresh_from_db()
        self.assertNotEqual(self.test_user.password, password_hash)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self.test_user)
        self.assertEqual(events[0].target, self.test_user)
        self.assertEqual(events[0].verb, event_user_edited.id)

    def test_user_multiple_set_password_view_no_permission(self):
        self._create_test_user()
        password_hash = self.test_user.password

        self._clear_events()

        response = self._request_test_user_password_set_multiple_view(
            password=TEST_USER_PASSWORD_EDITED
        )
        self.assertEqual(response.status_code, 404)

        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.password, password_hash)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_multiple_set_password_view_with_access(self):
        self._create_test_user()
        self.grant_access(obj=self.test_user, permission=permission_user_edit)

        password_hash = self.test_user.password

        self._clear_events()

        response = self._request_test_user_password_set_multiple_view(
            password=TEST_USER_PASSWORD_EDITED
        )
        self.assertEqual(response.status_code, 302)

        self.test_user.refresh_from_db()
        self.assertNotEqual(self.test_user.password, password_hash)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self.test_user)
        self.assertEqual(events[0].target, self.test_user)
        self.assertEqual(events[0].verb, event_user_edited.id)
