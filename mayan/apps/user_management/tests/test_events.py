from __future__ import unicode_literals

from actstream.models import Action

from mayan.apps.common.tests import GenericViewTestCase
from mayan.apps.rest_api.tests import BaseAPITestCase

from ..permissions import (
    permission_group_create, permission_group_edit, permission_user_create,
    permission_user_edit
)

from ..events import (
    event_group_created, event_group_edited, event_user_created,
    event_user_edited
)

from .mixins import (
    GroupAPITestMixin, GroupTestMixin, GroupViewTestMixin, UserAPITestMixin,
    UserTestMixin, UserViewTestMixin
)


class GroupEventsTestCase(GroupTestMixin, GroupViewTestMixin, UserTestMixin, GenericViewTestCase):
    def test_group_create_event(self):
        Action.objects.all().delete()

        self.grant_permission(
            permission=permission_group_create
        )
        self._request_test_group_create_view()

        self.assertEqual(Action.objects.last().target, self.test_group)
        self.assertEqual(Action.objects.last().verb, event_group_created.id)

    def test_group_edit_event(self):
        self._create_test_group()
        Action.objects.all().delete()

        self.grant_access(
            obj=self.test_group, permission=permission_group_edit
        )
        self._request_test_group_edit_view()

        self.assertEqual(Action.objects.last().target, self.test_group)
        self.assertEqual(Action.objects.last().verb, event_group_edited.id)


class GroupEventsAPITestCase(GroupAPITestMixin, GroupTestMixin, GroupViewTestMixin, BaseAPITestCase):
    def test_group_create_event_from_api_view(self):
        Action.objects.all().delete()

        self.grant_permission(
            permission=permission_group_create
        )
        self._request_test_group_create_api_view()

        self.assertEqual(Action.objects.last().target, self.test_group)
        self.assertEqual(Action.objects.last().verb, event_group_created.id)

    def test_group_edit_event_from_api_view(self):
        self._create_test_group()
        Action.objects.all().delete()

        self.grant_access(
            obj=self.test_group, permission=permission_group_edit
        )
        self._request_test_group_edit_patch_api_view()

        self.assertEqual(Action.objects.last().target, self.test_group)
        self.assertEqual(Action.objects.last().verb, event_group_edited.id)


class UserEventsTestCase(UserAPITestMixin, UserTestMixin, UserViewTestMixin, GenericViewTestCase):
    def test_user_create_event_from_view(self):
        Action.objects.all().delete()

        self.grant_permission(
            permission=permission_user_create
        )
        self._request_test_user_create_view()

        self.assertEqual(Action.objects.last().target, self.test_user)
        self.assertEqual(Action.objects.last().verb, event_user_created.id)

    def test_user_edit_event_from_view(self):
        self._create_test_user()
        Action.objects.all().delete()

        self.grant_access(
            obj=self.test_user, permission=permission_user_edit
        )
        self._request_test_user_edit_view()

        self.assertEqual(Action.objects.last().target, self.test_user)
        self.assertEqual(Action.objects.last().verb, event_user_edited.id)


class UserEventsAPITestCase(UserAPITestMixin, UserTestMixin, UserViewTestMixin, BaseAPITestCase):
    def test_user_create_event_from_api_view(self):
        Action.objects.all().delete()

        self.grant_permission(
            permission=permission_user_create
        )
        self._request_test_user_create_api_view()

        self.assertEqual(Action.objects.last().target, self.test_user)
        self.assertEqual(Action.objects.last().verb, event_user_created.id)

    def test_user_edit_event_from_api_view(self):
        self._create_test_user()
        Action.objects.all().delete()

        self.grant_access(
            obj=self.test_user, permission=permission_user_edit
        )
        self._request_test_user_edit_patch_api_view()

        self.assertEqual(Action.objects.last().target, self.test_user)
        self.assertEqual(Action.objects.last().verb, event_user_edited.id)
