from __future__ import unicode_literals

from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied

from mayan.apps.common.tests.base import BaseTestCase
from mayan.apps.user_management.tests.mixins import GroupTestMixin

from ..classes import Permission, PermissionNamespace
from ..models import StoredPermission

from .literals import (
    TEST_INVALID_PERMISSION_NAME, TEST_INVALID_PERMISSION_NAMESPACE_NAME,
    TEST_PERMISSION_LABEL, TEST_PERMISSION_NAME,
    TEST_PERMISSION_NAMESPACE_LABEL, TEST_PERMISSION_NAMESPACE_NAME
)
from .mixins import PermissionTestMixin, RoleTestMixin


class PermissionTestCase(
    GroupTestMixin, PermissionTestMixin, RoleTestMixin, BaseTestCase
):
    def setUp(self):
        super(PermissionTestCase, self).setUp()
        self._create_test_user()
        self._create_test_group()
        self._create_test_role()
        self._create_test_permission()

    def test_no_permissions(self):
        with self.assertRaises(PermissionDenied):
            Permission.check_user_permissions(
                permissions=(self.test_permission,), user=self.test_user
            )

    def test_with_permissions(self):
        self.test_group.user_set.add(self.test_user)
        self.test_role.grant(permission=self.test_permission)
        self.test_role.groups.add(self.test_group)

        try:
            Permission.check_user_permissions(
                permissions=(self.test_permission,), user=self.test_user
            )
        except PermissionDenied:
            self.fail('PermissionDenied exception was not expected.')

    def test_anonymous_user_permissions(self):
        self.auto_login_user = False
        test_anonymous_user = AnonymousUser()

        with self.assertRaises(PermissionDenied):
            Permission.check_user_permissions(
                permissions=(self.test_permission,), user=test_anonymous_user
            )


class StoredPermissionManagerTestCase(BaseTestCase):
    create_test_case_superuser = False
    create_test_case_user = False

    def test_purge_obsolete_with_invalid(self):
        StoredPermission.objects.create(
            namespace=TEST_INVALID_PERMISSION_NAMESPACE_NAME,
            name=TEST_INVALID_PERMISSION_NAME
        )

        StoredPermission.objects.purge_obsolete()

        self.assertEqual(StoredPermission.objects.count(), 0)

    def test_purge_obsolete_with_valid(self):
        test_permission_namespace = PermissionNamespace(
            label=TEST_PERMISSION_NAMESPACE_LABEL,
            name=TEST_PERMISSION_NAMESPACE_NAME
        )
        test_permission = test_permission_namespace.add_permission(
            label=TEST_PERMISSION_LABEL, name=TEST_PERMISSION_NAME
        )
        test_permission.stored_permission

        StoredPermission.objects.purge_obsolete()

        self.assertEqual(StoredPermission.objects.count(), 1)
