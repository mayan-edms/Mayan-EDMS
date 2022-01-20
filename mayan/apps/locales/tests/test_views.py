from mayan.apps.authentication.tests.mixins import LoginViewTestMixin, LogoutViewTestMixin
from mayan.apps.testing.tests.base import GenericViewTestCase
from mayan.apps.user_management.permissions import (
    permission_user_edit, permission_user_view
)

from ..events import event_user_locale_profile_edited

from .mixins import UserLocaleProfileViewMixin
from .literals import TEST_TRANSLATED_WORD


class CurrentUserViewTestCase(
    UserLocaleProfileViewMixin, GenericViewTestCase
):
    def test_current_user_locale_profile_detail_view_no_permission(self):
        self._clear_events()

        response = self._request_test_current_user_locale_profile_detail_view()
        self.assertEqual(response.status_code, 200)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_current_user_locale_profile_edit_view_no_permission(self):
        language = self._test_case_user.locale_profile.language
        timezone = self._test_case_user.locale_profile.timezone

        self._clear_events()

        response = self._request_test_current_user_locale_profile_edit_view()
        self.assertEqual(response.status_code, 302)

        self._test_case_user.refresh_from_db()
        self.assertNotEqual(
            self._test_case_user.locale_profile.language, language
        )
        self.assertNotEqual(
            self._test_case_user.locale_profile.timezone, timezone
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_case_user)
        self.assertEqual(events[0].verb, event_user_locale_profile_edited.id)


class SuperUserLocaleViewTestCase(
    UserLocaleProfileViewMixin, GenericViewTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_superuser()

    def test_superuser_locale_profile_detail_view_no_permission(self):
        self._clear_events()

        response = self._request_test_superuser_locale_profile_detail_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_superuser_locale_profile_detail_view_with_access(self):
        self.grant_access(
            obj=self.test_superuser, permission=permission_user_view
        )

        self._clear_events()

        response = self._request_test_superuser_locale_profile_detail_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_superuser_locale_profile_edit_view_no_permission(self):
        language = self.test_superuser.locale_profile.language
        timezone = self.test_superuser.locale_profile.timezone

        self._clear_events()

        response = self._request_test_superuser_locale_profile_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_superuser.refresh_from_db()
        self.assertEqual(
            self.test_superuser.locale_profile.language, language
        )
        self.assertEqual(
            self.test_superuser.locale_profile.timezone, timezone
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_superuser_locale_profile_edit_view_with_access(self):
        language = self.test_superuser.locale_profile.language
        timezone = self.test_superuser.locale_profile.timezone

        self.grant_access(
            obj=self.test_superuser, permission=permission_user_edit
        )

        self._clear_events()

        response = self._request_test_superuser_locale_profile_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_superuser.refresh_from_db()
        self.assertEqual(
            self.test_superuser.locale_profile.language, language
        )
        self.assertEqual(
            self.test_superuser.locale_profile.timezone, timezone
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class UserLocaleProfileViewTestCase(
    UserLocaleProfileViewMixin, GenericViewTestCase
):
    auto_create_test_user = True

    def test_user_locale_profile_detail_view_no_permission(self):
        self._clear_events()

        response = self._request_test_user_locale_profile_detail_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_locale_profile_detail_view_with_access(self):
        self.grant_access(
            obj=self.test_user, permission=permission_user_view
        )

        self._clear_events()

        response = self._request_test_user_locale_profile_detail_view()
        self.assertEqual(response.status_code, 200)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_locale_profile_edit_view_no_permission(self):
        language = self.test_user.locale_profile.language
        timezone = self.test_user.locale_profile.timezone

        self._clear_events()

        response = self._request_test_user_locale_profile_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.locale_profile.language, language)
        self.assertEqual(self.test_user.locale_profile.timezone, timezone)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_locale_profile_edit_view_with_access(self):
        language = self.test_user.locale_profile.language
        timezone = self.test_user.locale_profile.timezone

        self.grant_access(
            obj=self.test_user, permission=permission_user_edit
        )

        self._clear_events()

        response = self._request_test_user_locale_profile_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_user.refresh_from_db()
        self.assertNotEqual(self.test_user.locale_profile.language, language)
        self.assertNotEqual(self.test_user.locale_profile.timezone, timezone)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self.test_user)
        self.assertEqual(events[0].verb, event_user_locale_profile_edited.id)


class LanguageSelectionViewTestCase(
    LoginViewTestMixin, LogoutViewTestMixin, UserLocaleProfileViewMixin,
    GenericViewTestCase
):
    def test_language_change_view(self):
        response = self._request_test_current_user_locale_profile_edit_view(
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        response = self._request_test_current_user_locale_profile_detail_view()
        self.assertContains(
            response=response, text=TEST_TRANSLATED_WORD, status_code=200
        )

    def test_language_change_after_login_view(self):
        response = self._request_test_current_user_locale_profile_edit_view(
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        request = self._request_logout_view()
        self.assertEqual(request.status_code, 302)

        response = self._request_simple_login_view()
        self.assertEqual(request.status_code, 302)

        response = self._request_test_current_user_locale_profile_detail_view()
        self.assertContains(
            response=response, text=TEST_TRANSLATED_WORD, status_code=200
        )
