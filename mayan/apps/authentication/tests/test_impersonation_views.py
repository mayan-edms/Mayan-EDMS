from mayan.apps.testing.tests.base import GenericViewTestCase

from ..events import (
    event_user_impersonation_ended, event_user_impersonation_started
)
from ..literals import USER_IMPERSONATE_VARIABLE_DISABLE
from ..permissions import permission_users_impersonate

from .mixins import UserImpersonationViewTestMixin


class UserImpersonationViewTestCase(
    UserImpersonationViewTestMixin, GenericViewTestCase
):
    def test_user_impersonate_form_start_view_no_permission(self):
        self._create_test_user()

        self._clear_events()

        response = self._request_test_user_impersonate_form_start_view()
        self.assertEqual(response.status_code, 200)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

        self.expected_content_types = ('application/json',)

        self._clear_events()

        response = self.get(viewname='rest_api:user-current')
        self.assertEqual(response.data['id'], self._test_case_user.pk)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_impersonate_form_start_view_with_access(self):
        self._create_test_user()

        self.grant_access(
            obj=self._test_user, permission=permission_users_impersonate
        )

        self._clear_events()

        response = self._request_test_user_impersonate_form_start_view()
        self.assertEqual(response.status_code, 200)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_user)
        self.assertEqual(events[0].verb, event_user_impersonation_started.id)

        self.expected_content_types = ('application/json',)

        self._clear_events()

        response = self.get(viewname='rest_api:user-current')
        self.assertEqual(response.data['id'], self._test_user.pk)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_impersonate_end_view_no_permission(self):
        self._create_test_user()

        self._impersonate_test_user()

        self.grant_access(
            obj=self._test_user, permission=permission_users_impersonate
        )

        self.expected_content_types = ('application/json',)

        self._clear_events()

        response = self.get(viewname='rest_api:user-current')
        self.assertEqual(response.data['id'], self._test_user.pk)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

        self.revoke_access(
            obj=self._test_user, permission=permission_users_impersonate
        )

        self.expected_content_types = ('text/html; charset=utf-8',)

        self._clear_events()

        response = self._request_test_user_impersonate_end_view()
        self.assertEqual(response.status_code, 200)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

        self.expected_content_types = ('application/json',)

        self._clear_events()

        response = self.get(viewname='rest_api:user-current')
        self.assertEqual(response.data['id'], self._test_case_user.pk)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_impersonate_end_view_with_access(self):
        self._create_test_user()

        self._impersonate_test_user()

        self.grant_access(
            obj=self._test_user, permission=permission_users_impersonate
        )

        self.expected_content_types = ('application/json',)

        self._clear_events()

        response = self.get(viewname='rest_api:user-current')
        self.assertEqual(response.data['id'], self._test_user.pk)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

        self.expected_content_types = ('text/html; charset=utf-8',)

        self._clear_events()

        response = self._request_test_user_impersonate_end_view()
        self.assertEqual(response.status_code, 200)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_user)
        self.assertEqual(events[0].verb, event_user_impersonation_ended.id)

        self.expected_content_types = ('application/json',)

        self._clear_events()

        response = self.get(viewname='rest_api:user-current')
        self.assertEqual(response.data['id'], self._test_case_user.pk)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_session_impersonate_set_with_acess(self):
        self._create_test_user()

        self.grant_access(
            obj=self._test_user, permission=permission_users_impersonate
        )

        self._impersonate_test_user()

        self.expected_content_types = ('application/json',)

        self._clear_events()

        response = self.get(viewname='rest_api:user-current')
        self.assertEqual(response.data['id'], self._test_user.pk)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_session_impersonate_unset_with_access(self):
        self._create_test_user()
        self.grant_access(
            obj=self._test_user, permission=permission_users_impersonate
        )

        self._impersonate_test_user()

        self.expected_content_types = ('application/json',)

        self._clear_events()

        response = self.get(
            viewname='rest_api:user-current', query={
                USER_IMPERSONATE_VARIABLE_DISABLE: ''
            }
        )
        self.assertEqual(response.data['id'], self._test_case_user.pk)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_user)
        self.assertEqual(events[0].verb, event_user_impersonation_ended.id)

    def test_user_impersonate_start_view_no_permission(self):
        self._create_test_user()

        self._clear_events()

        response = self._request_test_user_impersonate_start_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

        self.expected_content_types = ('application/json',)

        self._clear_events()

        response = self.get(viewname='rest_api:user-current')
        self.assertEqual(response.data['id'], self._test_case_user.pk)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_user_impersonate_start_view_with_access(self):
        self._create_test_user()

        self.grant_access(
            obj=self._test_user, permission=permission_users_impersonate
        )

        self._clear_events()

        response = self._request_test_user_impersonate_start_view()
        self.assertEqual(response.status_code, 200)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_user)
        self.assertEqual(events[0].verb, event_user_impersonation_started.id)

        self.expected_content_types = ('application/json',)

        self._clear_events()

        response = self.get(viewname='rest_api:user-current')
        self.assertEqual(response.data['id'], self._test_user.pk)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
