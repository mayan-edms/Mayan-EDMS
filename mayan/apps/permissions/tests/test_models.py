from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.test import TestCase

from organizations.utils import create_default_organization
from user_management.models import MayanGroup
from user_management.tests import TEST_GROUP, TEST_USER_USERNAME

from ..classes import Permission
from ..models import Role, StoredPermission
from ..permissions import permission_role_view

from .literals import TEST_ROLE_LABEL


class PermissionTestCase(TestCase):
    def setUp(self):
        create_default_organization()
        self.user = get_user_model().on_organization.create(
            username=TEST_USER_USERNAME
        )
        self.group = MayanGroup.on_organization.create(name=TEST_GROUP)
        self.role = Role.on_organization.create(label=TEST_ROLE_LABEL)
        Permission.invalidate_cache()

    def test_no_permissions(self):
        with self.assertRaises(PermissionDenied):
            Permission.check_permissions(
                requester=self.user, permissions=(permission_role_view,)
            )

    def test_with_permissions(self):
        self.group.users.add(self.user)
        self.role.permissions.add(permission_role_view.stored_permission)
        self.role.organization_groups.add(self.group)

        try:
            Permission.check_permissions(
                requester=self.user, permissions=(permission_role_view,)
            )
        except PermissionDenied:
            self.fail('PermissionDenied exception was not expected.')
