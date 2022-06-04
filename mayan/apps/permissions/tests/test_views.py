from mayan.apps.testing.tests.base import GenericViewTestCase
from mayan.apps.user_management.permissions import permission_group_edit
from mayan.apps.user_management.tests.mixins import GroupTestMixin

from ..events import event_role_created, event_role_edited
from ..models import Role
from ..permissions import (
    permission_role_create, permission_role_delete, permission_role_edit,
    permission_role_view
)

from .mixins import (
    GroupRoleAddRemoveViewTestMixin, RoleGroupAddRemoveViewTestMixin,
    RolePermissionAddRemoveViewTestMixin, RoleTestMixin, RoleViewTestMixin
)


class RoleViewTestCase(
    RoleTestMixin, RoleViewTestMixin, GenericViewTestCase
):
    def test_role_creation_view_no_permission(self):
        role_count = Role.objects.count()

        self._clear_events()

        response = self._request_test_role_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(Role.objects.count(), role_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_role_creation_view_with_permission(self):
        self.grant_permission(permission=permission_role_create)
        role_count = Role.objects.count()

        self._clear_events()

        response = self._request_test_role_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Role.objects.count(), role_count + 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_role)
        self.assertEqual(events[0].verb, event_role_created.id)

    def test_role_single_delete_view_no_permission(self):
        self._create_test_role()

        role_count = Role.objects.count()

        self._clear_events()

        response = self._request_test_role_single_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Role.objects.count(), role_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_role_single_delete_view_with_access(self):
        self._create_test_role()

        self.grant_access(
            obj=self._test_role, permission=permission_role_delete
        )

        role_count = Role.objects.count()

        self._clear_events()

        response = self._request_test_role_single_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Role.objects.count(), role_count - 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_role_multiple_delete_view_no_permission(self):
        self._create_test_role()

        role_count = Role.objects.count()

        self._clear_events()

        response = self._request_test_role_multiple_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Role.objects.count(), role_count)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_role_multiple_delete_view_with_access(self):
        self._create_test_role()

        role_count = Role.objects.count()

        self.grant_access(
            obj=self._test_role, permission=permission_role_delete
        )

        self._clear_events()

        response = self._request_test_role_multiple_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Role.objects.count(), role_count - 1)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_role_edit_view_no_permission(self):
        self._create_test_role()
        role_label = self._test_role.label

        self._clear_events()

        response = self._request_test_role_edit_view()

        self.assertEqual(response.status_code, 404)

        self._test_role.refresh_from_db()
        self.assertEqual(self._test_role.label, role_label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_role_edit_view_with_access(self):
        self._create_test_role()
        self.grant_access(obj=self._test_role, permission=permission_role_edit)

        role_label = self._test_role.label

        self._clear_events()

        response = self._request_test_role_edit_view()
        self.assertEqual(response.status_code, 302)

        self._test_role.refresh_from_db()
        self.assertNotEqual(self._test_role.label, role_label)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_role)
        self.assertEqual(events[0].verb, event_role_edited.id)

    def test_role_list_view_no_permission(self):
        self._create_test_role()

        self._clear_events()

        response = self._request_test_role_list_view()
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(
            response=response, text=self._test_role.label, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_role_list_view_with_access(self):
        self._create_test_role()
        self.grant_access(obj=self._test_role, permission=permission_role_view)

        self._clear_events()

        response = self._request_test_role_list_view()
        self.assertContains(
            response=response, text=self._test_role.label, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class RoleGroupAddRemoveViewTestCase(
    GroupTestMixin, RoleGroupAddRemoveViewTestMixin, RoleTestMixin,
    GenericViewTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_role()
        self._create_test_group()

    def test_role_group_add_remove_get_view_no_permission(self):
        self._test_role.groups.add(self._test_group)

        self._clear_events()

        response = self._request_test_role_group_add_remove_get_view()
        self.assertNotContains(
            response=response, text=str(self._test_role),
            status_code=404
        )
        self.assertNotContains(
            response=response, text=str(self._test_group),
            status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_role_group_add_remove_get_view_with_role_access(self):
        self._test_role.groups.add(self._test_group)

        self.grant_access(
            obj=self._test_role,
            permission=permission_role_edit
        )

        self._clear_events()

        response = self._request_test_role_group_add_remove_get_view()
        self.assertContains(
            response=response, text=str(self._test_role),
            status_code=200
        )
        self.assertNotContains(
            response=response, text=str(self._test_group),
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_role_group_add_remove_get_view_with_group_access(self):
        self._test_role.groups.add(self._test_group)

        self.grant_access(
            obj=self._test_group,
            permission=permission_group_edit
        )

        self._clear_events()

        response = self._request_test_role_group_add_remove_get_view()
        self.assertNotContains(
            response=response, text=str(self._test_role),
            status_code=404
        )
        self.assertNotContains(
            response=response, text=str(self._test_group),
            status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_role_group_add_remove_get_view_with_full_access(self):
        self._test_role.groups.add(self._test_group)

        self.grant_access(
            obj=self._test_role,
            permission=permission_role_edit
        )
        self.grant_access(
            obj=self._test_group,
            permission=permission_group_edit
        )

        self._clear_events()

        response = self._request_test_role_group_add_remove_get_view()
        self.assertContains(
            response=response, text=str(self._test_role),
            status_code=200
        )
        self.assertContains(
            response=response, text=str(self._test_group),
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_role_group_add_view_no_permission(self):
        self._clear_events()

        response = self._request_test_role_group_add_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self._test_group not in self._test_role.groups.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_role_group_add_view_with_role_access(self):
        self.grant_access(
            obj=self._test_role,
            permission=permission_role_edit
        )

        self._clear_events()

        response = self._request_test_role_group_add_view()
        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            self._test_group not in self._test_role.groups.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_role_group_add_view_with_group_access(self):
        self.grant_access(
            obj=self._test_group,
            permission=permission_group_edit
        )

        self._clear_events()

        response = self._request_test_role_group_add_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self._test_group not in self._test_role.groups.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_role_group_add_view_with_full_access(self):
        self.grant_access(
            obj=self._test_role,
            permission=permission_role_edit
        )
        self.grant_access(
            obj=self._test_group,
            permission=permission_group_edit
        )

        self._clear_events()

        response = self._request_test_role_group_add_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            self._test_group in self._test_role.groups.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self._test_group)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_role)
        self.assertEqual(events[0].verb, event_role_edited.id)

    def test_role_group_remove_view_no_permission(self):
        self._test_role.groups.add(self._test_group)

        self._clear_events()

        response = self._request_test_role_group_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self._test_group in self._test_role.groups.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_role_group_remove_view_with_role_access(self):
        self._test_role.groups.add(self._test_group)

        self.grant_access(
            obj=self._test_role,
            permission=permission_role_edit
        )

        self._clear_events()

        response = self._request_test_role_group_remove_view()
        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            self._test_group in self._test_role.groups.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_role_group_remove_view_with_group_access(self):
        self._test_role.groups.add(self._test_group)

        self.grant_access(
            obj=self._test_group,
            permission=permission_group_edit
        )

        self._clear_events()

        response = self._request_test_role_group_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self._test_group in self._test_role.groups.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_role_group_remove_view_with_full_access(self):
        self._test_role.groups.add(self._test_group)

        self.grant_access(
            obj=self._test_role,
            permission=permission_role_edit
        )
        self.grant_access(
            obj=self._test_group,
            permission=permission_group_edit
        )

        self._clear_events()

        response = self._request_test_role_group_remove_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            self._test_group not in self._test_role.groups.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self._test_group)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_role)
        self.assertEqual(events[0].verb, event_role_edited.id)


class RolePermissionAddRemoveViewTestCase(
    RolePermissionAddRemoveViewTestMixin, RoleTestMixin, GenericViewTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_role()
        self._create_test_permission()

    def test_role_permission_add_remove_get_view_no_permission(self):
        self._test_role.permissions.add(self._test_permission.stored_permission)

        self._clear_events()

        response = self._request_test_role_permission_add_remove_get_view()
        self.assertNotContains(
            response=response, text=str(self._test_role),
            status_code=404
        )
        self.assertNotContains(
            response=response, text=str(self._test_permission),
            status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_role_permission_add_remove_get_view_with_access(self):
        """
        Tests that a defined permission is available before it is ever used
        or referenced. Tests the runtime permission to stored permission
        cache initialization.
        https://forum.mayan-edms.com/viewtopic.php?f=7&t=1614
        GitLab issue #757 "Permissions list does not show an object until
        one has been created"
        """
        self._test_role.permissions.add(self._test_permission.stored_permission)

        self.grant_access(
            obj=self._test_role,
            permission=permission_role_edit
        )

        self._clear_events()

        response = self._request_test_role_permission_add_remove_get_view()
        self.assertContains(
            response=response, text=str(self._test_role),
            status_code=200
        )
        self.assertContains(
            response=response, text=str(self._test_permission),
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_role_permission_add_view_no_permission(self):
        self._clear_events()

        response = self._request_test_role_permission_add_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self._test_permission.stored_permission not in self._test_role.permissions.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_role_permission_add_view_with_access(self):
        self.grant_access(
            obj=self._test_role,
            permission=permission_role_edit
        )

        self._clear_events()

        response = self._request_test_role_permission_add_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            self._test_permission.stored_permission in self._test_role.permissions.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(
            events[0].action_object, self._test_permission.stored_permission
        )
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_role)
        self.assertEqual(events[0].verb, event_role_edited.id)

    def test_role_permission_remove_view_no_permission(self):
        self._test_role.permissions.add(self._test_permission.stored_permission)

        self._clear_events()

        response = self._request_test_role_permission_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self._test_permission.stored_permission in self._test_role.permissions.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_role_permission_remove_view_with_access(self):
        self._test_role.permissions.add(self._test_permission.stored_permission)

        self.grant_access(
            obj=self._test_role,
            permission=permission_role_edit
        )

        self._clear_events()

        response = self._request_test_role_permission_remove_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            self._test_permission.stored_permission not in self._test_role.permissions.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(
            events[0].action_object, self._test_permission.stored_permission
        )
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_role)
        self.assertEqual(events[0].verb, event_role_edited.id)


class GroupRoleAddRemoveViewTestCase(
    GroupTestMixin, GroupRoleAddRemoveViewTestMixin, RoleTestMixin,
    GenericViewTestCase
):
    def setUp(self):
        super().setUp()
        self._create_test_group()
        self._create_test_role()

    def test_group_role_add_remove_get_view_no_permission(self):
        self._test_group.roles.add(self._test_role)

        self._clear_events()

        response = self._request_test_group_role_add_remove_get_view()
        self.assertNotContains(
            response=response, text=str(self._test_group),
            status_code=404
        )
        self.assertNotContains(
            response=response, text=str(self._test_role),
            status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_role_add_remove_get_view_with_group_access(self):
        self._test_group.roles.add(self._test_role)

        self.grant_access(
            obj=self._test_group,
            permission=permission_group_edit
        )

        self._clear_events()

        response = self._request_test_group_role_add_remove_get_view()
        self.assertContains(
            response=response, text=str(self._test_group),
            status_code=200
        )
        self.assertNotContains(
            response=response, text=str(self._test_role),
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_role_add_remove_get_view_with_role_access(self):
        self._test_group.roles.add(self._test_role)

        self.grant_access(
            obj=self._test_role,
            permission=permission_role_edit
        )

        self._clear_events()

        response = self._request_test_group_role_add_remove_get_view()
        self.assertNotContains(
            response=response, text=str(self._test_group),
            status_code=404
        )
        self.assertNotContains(
            response=response, text=str(self._test_role),
            status_code=404
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_role_add_remove_get_view_with_full_access(self):
        self._test_group.roles.add(self._test_role)

        self.grant_access(
            obj=self._test_group,
            permission=permission_group_edit
        )
        self.grant_access(
            obj=self._test_role,
            permission=permission_role_edit
        )

        self._clear_events()

        response = self._request_test_group_role_add_remove_get_view()
        self.assertContains(
            response=response, text=str(self._test_group),
            status_code=200
        )
        self.assertContains(
            response=response, text=str(self._test_role),
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_role_add_view_no_permission(self):
        self._clear_events()

        response = self._request_test_group_role_add_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self._test_role not in self._test_group.roles.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_role_add_view_with_group_access(self):
        self.grant_access(
            obj=self._test_group,
            permission=permission_group_edit
        )

        self._clear_events()

        response = self._request_test_group_role_add_view()
        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            self._test_role not in self._test_group.roles.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_role_add_view_with_role_access(self):
        self.grant_access(
            obj=self._test_role,
            permission=permission_role_edit
        )

        self._clear_events()

        response = self._request_test_group_role_add_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self._test_role not in self._test_group.roles.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_role_add_view_with_full_access(self):
        self.grant_access(
            obj=self._test_group,
            permission=permission_group_edit
        )
        self.grant_access(
            obj=self._test_role,
            permission=permission_role_edit
        )

        self._clear_events()

        response = self._request_test_group_role_add_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            self._test_role in self._test_group.roles.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self._test_group)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_role)
        self.assertEqual(events[0].verb, event_role_edited.id)

    def test_group_role_remove_view_no_permission(self):
        self._test_group.roles.add(self._test_role)

        self._clear_events()

        response = self._request_test_group_role_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self._test_role in self._test_group.roles.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_role_remove_view_with_group_access(self):
        self._test_group.roles.add(self._test_role)

        self.grant_access(
            obj=self._test_group,
            permission=permission_group_edit
        )

        self._clear_events()

        response = self._request_test_group_role_remove_view()
        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            self._test_role in self._test_group.roles.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_role_remove_view_with_role_access(self):
        self._test_group.roles.add(self._test_role)

        self.grant_access(
            obj=self._test_role,
            permission=permission_role_edit
        )

        self._clear_events()

        response = self._request_test_group_role_remove_view()
        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            self._test_role in self._test_group.roles.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_group_role_remove_view_with_full_access(self):
        self._test_group.roles.add(self._test_role)

        self.grant_access(
            obj=self._test_group,
            permission=permission_group_edit
        )
        self.grant_access(
            obj=self._test_role,
            permission=permission_role_edit
        )

        self._clear_events()

        response = self._request_test_group_role_remove_view()
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            self._test_role not in self._test_group.roles.all()
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self._test_group)
        self.assertEqual(events[0].actor, self._test_case_user)
        self.assertEqual(events[0].target, self._test_role)
        self.assertEqual(events[0].verb, event_role_edited.id)
