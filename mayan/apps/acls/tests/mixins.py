from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from acls.models import AccessControlList
from permissions.models import Role
from permissions.tests.literals import TEST_ROLE_LABEL
from permissions.tests.mixins import RoleTestCaseMixin
from user_management.tests.literals import (
    TEST_ADMIN_PASSWORD, TEST_ADMIN_USERNAME, TEST_ADMIN_EMAIL,
    TEST_GROUP_NAME, TEST_USER_EMAIL, TEST_USER_USERNAME, TEST_USER_PASSWORD
)


class ACLTestCaseMixin(RoleTestCaseMixin):
    def setUp(self):
        super(ACLTestCaseMixin, self).setUp()
        self.admin_user = get_user_model().objects.create_superuser(
            username=TEST_ADMIN_USERNAME, email=TEST_ADMIN_EMAIL,
            password=TEST_ADMIN_PASSWORD
        )

        self.user = get_user_model().objects.create_user(
            username=TEST_USER_USERNAME, email=TEST_USER_EMAIL,
            password=TEST_USER_PASSWORD
        )

        self.group = Group.objects.create(name=TEST_GROUP_NAME)
        self.role = Role.objects.create(label=TEST_ROLE_LABEL)
        self.group.user_set.add(self.user)
        self.role.groups.add(self.group)

    def grant_access(self, permission, obj):
        AccessControlList.objects.grant(
            permission=permission, role=self.role, obj=obj
        )
