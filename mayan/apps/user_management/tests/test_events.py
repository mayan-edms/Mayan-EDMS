from actstream.models import Action

from mayan.apps.tests.tests.base import GenericViewTestCase
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..permissions import (
    permission_group_create, permission_group_edit, permission_user_create,
    permission_user_edit
)

from ..events import (
    event_group_created, event_group_edited, event_user_created,
    event_user_edited, event_user_logged_in, event_user_logged_out
)

from .mixins import (
    GroupAPIViewTestMixin, GroupTestMixin, GroupViewTestMixin,
    UserAPIViewTestMixin, UserViewTestMixin
)


class GroupEventsViewTestCase(
    GroupTestMixin, GroupViewTestMixin, GenericViewTestCase
):
    def test_group_create_event(self):
        self.grant_permission(
            permission=permission_group_create
        )
        Action.objects.all().delete()

        response = self._request_test_group_create_view()
        self.assertEqual(response.status_code, 302)

        action = Action.objects.last()

        self.assertEqual(action.actor, self._test_case_user)
        self.assertEqual(action.target, self.test_group)
        self.assertEqual(action.verb, event_group_created.id)

    def test_group_edit_event(self):
        self._create_test_group()
        self.grant_access(
            obj=self.test_group, permission=permission_group_edit
        )
        Action.objects.all().delete()

        response = self._request_test_group_edit_view()
        self.assertEqual(response.status_code, 302)

        action = Action.objects.last()

        self.assertEqual(action.target, self.test_group)
        self.assertEqual(action.verb, event_group_edited.id)


class GroupEventsAPITestCase(
    GroupAPIViewTestMixin, GroupTestMixin, GroupViewTestMixin,
    BaseAPITestCase
):
    def test_group_create_event_from_api_view(self):
        self.grant_permission(
            permission=permission_group_create
        )
        Action.objects.all().delete()

        response = self._request_test_group_create_api_view()
        self.assertEqual(response.status_code, 201)

        action = Action.objects.last()

        self.assertEqual(action.actor, self.test_group)
        self.assertEqual(action.target, self.test_group)
        self.assertEqual(action.verb, event_group_created.id)

    def test_group_edit_event_from_api_view(self):
        self._create_test_group()

        self.grant_access(
            obj=self.test_group, permission=permission_group_edit
        )
        Action.objects.all().delete()

        response = self._request_test_group_edit_patch_api_view()
        self.assertEqual(response.status_code, 200)

        action = Action.objects.last()

        self.assertEqual(action.actor, self.test_group)
        self.assertEqual(action.target, self.test_group)
        self.assertEqual(action.verb, event_group_edited.id)


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


class UserEventsViewTestCase(
    UserAPIViewTestMixin, UserViewTestMixin, GenericViewTestCase
):
    def test_user_create_event_from_view(self):
        self.grant_permission(
            permission=permission_user_create
        )
        Action.objects.all().delete()

        response = self._request_test_user_create_view()
        self.assertEqual(response.status_code, 302)

        action = Action.objects.last()

        self.assertEqual(action.actor, self._test_case_user)
        self.assertEqual(action.target, self.test_user)
        self.assertEqual(action.verb, event_user_created.id)

    def test_user_edit_event_from_view(self):
        self._create_test_user()

        self.grant_access(
            obj=self.test_user, permission=permission_user_edit
        )
        Action.objects.all().delete()

        response = self._request_test_user_edit_view()
        self.assertEqual(response.status_code, 302)

        action = Action.objects.last()

        self.assertEqual(action.actor, self._test_case_user)
        self.assertEqual(action.target, self.test_user)
        self.assertEqual(action.verb, event_user_edited.id)


class UserEventsAPITestCase(
    UserAPIViewTestMixin, UserViewTestMixin, BaseAPITestCase
):
    def test_user_create_event_from_api_view(self):
        self.grant_permission(
            permission=permission_user_create
        )
        Action.objects.all().delete()

        response = self._request_test_user_create_api_view()
        self.assertEqual(response.status_code, 201)

        action = Action.objects.last()

        self.assertEqual(action.actor, self.test_user)
        self.assertEqual(action.target, self.test_user)
        self.assertEqual(action.verb, event_user_created.id)

    def test_user_edit_event_from_api_view(self):
        self._create_test_user()
        self.grant_access(
            obj=self.test_user, permission=permission_user_edit
        )
        Action.objects.all().delete()

        response = self._request_test_user_edit_patch_api_view()
        self.assertEqual(response.status_code, 200)

        action = Action.objects.last()

        self.assertEqual(action.actor, self.test_user)
        self.assertEqual(action.target, self.test_user)
        self.assertEqual(action.verb, event_user_edited.id)
