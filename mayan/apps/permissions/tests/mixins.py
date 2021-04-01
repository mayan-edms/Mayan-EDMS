from django.db.models import Q

from ..classes import Permission, PermissionNamespace
from ..models import Role

from .literals import (
    TEST_CASE_ROLE_LABEL, TEST_PERMISSION_LABEL, TEST_PERMISSION_LABEL_2,
    TEST_PERMISSION_NAME, TEST_PERMISSION_NAME_2, TEST_PERMISSION_NAMESPACE_LABEL,
    TEST_PERMISSION_NAMESPACE_LABEL_2, TEST_PERMISSION_NAMESPACE_NAME,
    TEST_PERMISSION_NAMESPACE_NAME_2, TEST_ROLE_LABEL, TEST_ROLE_LABEL_EDITED
)


class GroupRoleAddRemoveViewTestMixin:
    def _request_test_group_role_add_remove_get_view(self):
        return self.get(
            viewname='permissions:group_roles', kwargs={
                'group_id': self.test_group.pk
            }
        )

    def _request_test_group_role_add_view(self):
        return self.post(
            viewname='permissions:group_roles', kwargs={
                'group_id': self.test_group.pk,
            }, data={
                'available-submit': 'true',
                'available-selection': self.test_role.pk
            }
        )

    def _request_test_group_role_remove_view(self):
        return self.post(
            viewname='permissions:group_roles', kwargs={
                'group_id': self.test_group.pk,
            }, data={
                'added-submit': 'true',
                'added-selection': self.test_role.pk
            }
        )


class PermissionAPIViewTestMixin:
    def _request_permissions_list_api_view(self):
        return self.get(viewname='rest_api:permission-list')


class PermissionTestMixin:
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


class PermissionTestCaseMixin:
    def setUp(self):
        super().setUp()
        Permission.invalidate_cache()


class RoleAPIViewTestMixin:
    def _request_test_role_create_api_view(self, extra_data=None):
        pk_list = list(Role.objects.values_list('pk', flat=True))

        data = {
            'label': TEST_ROLE_LABEL
        }

        if extra_data:
            data.update(extra_data)

        response = self.post(
            viewname='rest_api:role-list', data=data
        )

        try:
            self.test_role = Role.objects.get(
                ~Q(pk__in=pk_list)
            )
        except Role.DoesNotExist:
            self.test_role = None

        return response

    def _request_test_role_delete_api_view(self):
        return self.delete(
            viewname='rest_api:role-detail', kwargs={
                'role_id': self.test_role.pk
            }
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
                'role_id': self.test_role.pk
            }, data=data
        )

    def _request_test_role_edit_api_patch_view_extra_data(self):
        extra_data = {
            'groups_pk_list': '{}'.format(self.test_group.pk),
            'permissions_pk_list': '{}'.format(self.test_permission.pk)
        }
        return self._request_test_role_edit_api_view(
            extra_data=extra_data, request_type='patch'
        )

    def _request_test_role_edit_api_put_view_extra_data(self):
        extra_data = {
            'groups_pk_list': '{}'.format(self.test_group.pk),
            'permissions_pk_list': '{}'.format(self.test_permission.pk)
        }
        return self._request_test_role_edit_api_view(
            extra_data=extra_data, request_type='put'
        )

    def _request_test_role_list_api_view(self):
        return self.get(viewname='rest_api:role-list')


class RoleGroupAPIViewTestMixin:
    def _request_test_role_group_add_api_view(self):
        return self.post(
            viewname='rest_api:role-group-add', kwargs={
                'role_id': self.test_role.pk
            }, data={'group': self.test_group.pk}
        )

    def _request_test_role_group_list_api_view(self):
        return self.get(
            viewname='rest_api:role-group-list', kwargs={
                'role_id': self.test_role.pk
            }
        )

    def _request_test_role_group_remove_api_view(self):
        return self.post(
            viewname='rest_api:role-group-remove', kwargs={
                'role_id': self.test_role.pk
            }, data={'group': self.test_group.pk}
        )


class RolePermissionAPIViewTestMixin:
    def _request_test_role_permission_add_api_view(self):
        return self.post(
            viewname='rest_api:role-permission-add', kwargs={
                'role_id': self.test_role.pk
            }, data={'permission': self.test_permission.pk}
        )

    def _request_test_role_permission_list_api_view(self):
        return self.get(
            viewname='rest_api:role-permission-list', kwargs={
                'role_id': self.test_role.pk
            }
        )

    def _request_test_role_permission_remove_api_view(self):
        return self.post(
            viewname='rest_api:role-permission-remove', kwargs={
                'role_id': self.test_role.pk
            }, data={'permission': self.test_permission.pk}
        )


class RoleTestCaseMixin:
    def setUp(self):
        super().setUp()
        if hasattr(self, '_test_case_group'):
            self.create_role()

    def create_role(self):
        self._test_case_role = Role.objects.create(label=TEST_CASE_ROLE_LABEL)

    def grant_permission(self, permission):
        self._test_case_role.grant(permission=permission)

    def revoke_permission(self, permission):
        self._test_case_role.revoke(permission=permission)


class RoleGroupAddRemoveViewTestMixin:
    def _request_test_role_group_add_remove_get_view(self):
        return self.get(
            viewname='permissions:role_groups', kwargs={
                'role_id': self.test_role.pk
            }
        )

    def _request_test_role_group_add_view(self):
        return self.post(
            viewname='permissions:role_groups', kwargs={
                'role_id': self.test_role.pk,
            }, data={
                'available-submit': 'true',
                'available-selection': self.test_group.pk
            }
        )

    def _request_test_role_group_remove_view(self):
        return self.post(
            viewname='permissions:role_groups', kwargs={
                'role_id': self.test_role.pk,
            }, data={
                'added-submit': 'true',
                'added-selection': self.test_group.pk
            }
        )


class RolePermissionAddRemoveViewTestMixin:
    def _request_test_role_permission_add_remove_get_view(self):
        return self.get(
            viewname='permissions:role_permissions', kwargs={
                'role_id': self.test_role.pk
            }
        )

    def _request_test_role_permission_add_view(self):
        return self.post(
            viewname='permissions:role_permissions', kwargs={
                'role_id': self.test_role.pk,
            }, data={
                'available-submit': 'true',
                'available-selection': self.test_permission.stored_permission.pk
            }
        )

    def _request_test_role_permission_remove_view(self):
        return self.post(
            viewname='permissions:role_permissions', kwargs={
                'role_id': self.test_role.pk,
            }, data={
                'added-submit': 'true',
                'added-selection': self.test_permission.stored_permission.pk
            }
        )


class RoleTestMixin:
    def setUp(self):
        super().setUp()
        self.test_roles = []

    def _create_test_role(self, add_groups=None):
        total_test_roles = len(self.test_roles)
        label = '{}_{}'.format(TEST_ROLE_LABEL, total_test_roles)

        self.test_role = Role.objects.create(label=label)

        self.test_roles.append(self.test_role)

        for group in add_groups or []:
            self.test_role.groups.add(group)


class RoleViewTestMixin:
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

    def _request_test_role_list_view(self):
        return self.get(viewname='permissions:role_list')
