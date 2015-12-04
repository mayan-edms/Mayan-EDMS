from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.test import TestCase

from user_management.tests import TEST_GROUP, TEST_USER_USERNAME

from ..classes import Permission
from ..models import Role
from ..permissions import permission_role_view

from .literals import TEST_ROLE_LABEL


class PermissionTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username=TEST_USER_USERNAME
        )
        self.group = Group.objects.create(name=TEST_GROUP)
        self.role = Role.objects.create(label=TEST_ROLE_LABEL)
        Permission.invalidate_cache()

    def test_no_permissions(self):
        with self.assertRaises(PermissionDenied):
            Permission.check_permissions(
                requester=self.user, permissions=(permission_role_view,)
            )

    def test_with_permissions(self):
        self.group.user_set.add(self.user)
        self.role.permissions.add(permission_role_view.stored_permission)
        self.role.groups.add(self.group)

        try:
            Permission.check_permissions(
                requester=self.user, permissions=(permission_role_view,)
            )
        except PermissionDenied:
            self.fail('PermissionDenied exception was not expected.')
