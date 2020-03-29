from ..classes import Permission, PermissionNamespace
from ..models import Role

from .literals import (
    TEST_CASE_ROLE_LABEL, TEST_PERMISSION_LABEL, TEST_PERMISSION_LABEL_2,
    TEST_PERMISSION_NAME, TEST_PERMISSION_NAME_2, TEST_PERMISSION_NAMESPACE_LABEL,
    TEST_PERMISSION_NAMESPACE_LABEL_2, TEST_PERMISSION_NAMESPACE_NAME,
    TEST_PERMISSION_NAMESPACE_NAME_2, TEST_ROLE_LABEL, TEST_ROLE_LABEL_EDITED
)


class GroupRoleViewTestMixin(object):
    def _request_test_group_roles_view(self):
        return self.get(
            viewname='permissions:group_roles', kwargs={
                'group_id': self.test_group.pk
            }
        )


class PermissionAPIViewTestMixin(object):
    def _request_permissions_list_api_view(self):
        return self.get(viewname='rest_api:permission-list')


class PermissionTestMixin(object):
    def _create_test_permission(self):
        self.test_permission_namespace = PermissionNamespace(
            label=TEST_PERMISSION_NAMESPACE_LABEL,
            name=TEST_PERMISSION_NAMESPACE_NAME
        )
        self.test_permission = self.test_permission_namespace.add_permission(
            label=TEST_PERMISSION_LABEL,
            name=TEST_PERMISSION_NAME
        )

    def _create_test_permission_2(self):
        self.test_permission_namespace_2 = PermissionNamespace(
            label=TEST_PERMISSION_NAMESPACE_LABEL_2,
            name=TEST_PERMISSION_NAMESPACE_NAME_2
        )
        self.test_permission_2 = self.test_permission_namespace_2.add_permission(
            label=TEST_PERMISSION_LABEL_2,
            name=TEST_PERMISSION_NAME_2
        )


class PermissionTestCaseMixin(object):
    def setUp(self):
        super(PermissionTestCaseMixin, self).setUp()
        Permission.invalidate_cache()


class RoleAPIViewTestMixin(object):
    def _request_test_role_create_api_view(self, extra_data=None):
        data = {
            'label': TEST_ROLE_LABEL
        }

        if extra_data:
            data.update(extra_data)

        return self.post(
            viewname='rest_api:role-list', data=data
        )

    def _request_test_role_delete_api_view(self):
        return self.delete(
            viewname='rest_api:role-detail', kwargs={'pk': self.test_role.pk}
        )

    def _request_test_role_edit_api_view(
        self, extra_data=None, request_type='patch'
    ):
        data = {
            'label': TEST_ROLE_LABEL_EDITED
        }

        if extra_data:
            data.update(extra_data)

        return getattr(self, request_type)(
            viewname='rest_api:role-detail', kwargs={
                'pk': self.test_role.pk
            }, data=data
        )

    def _request_role_list_api_view(self):
        return self.get(viewname='rest_api:role-list')


class RoleTestCaseMixin(object):
    def setUp(self):
        super(RoleTestCaseMixin, self).setUp()
        if hasattr(self, '_test_case_group'):
            self.create_role()

    def create_role(self):
        self._test_case_role = Role.objects.create(label=TEST_CASE_ROLE_LABEL)

    def grant_permission(self, permission):
        self._test_case_role.grant(permission=permission)

    def revoke_permission(self, permission):
        self._test_case_role.revoke(permission=permission)


class RoleTestMixin(object):
    def _create_test_role(self):
        self.test_role = Role.objects.create(label=TEST_ROLE_LABEL)


class RoleViewTestMixin(object):
    def _request_test_role_create_view(self):
        # Typecast to list to force queryset evaluation
        values = list(Role.objects.values_list('pk', flat=True))

        response = self.post(
            viewname='permissions:role_create', data={
                'label': TEST_ROLE_LABEL,
            }
        )

        self.test_role = Role.objects.exclude(pk__in=values).first()

        return response

    def _request_test_role_delete_view(self):
        return self.post(
            viewname='permissions:role_delete', kwargs={
                'role_id': self.test_role.pk
            }
        )

    def _request_test_role_edit_view(self):
        return self.post(
            viewname='permissions:role_edit', kwargs={
                'role_id': self.test_role.pk
            }, data={
                'label': TEST_ROLE_LABEL_EDITED,
            }
        )

    def _request_test_role_groups_view(self):
        return self.get(
            viewname='permissions:role_groups', kwargs={
                'role_id': self.test_role.pk
            }
        )

    def _request_test_role_list_view(self):
        return self.get(viewname='permissions:role_list')

    def _request_test_role_permissions_view(self):
        return self.get(
            viewname='permissions:role_permissions', kwargs={
                'role_id': self.test_role.pk
            }
        )
