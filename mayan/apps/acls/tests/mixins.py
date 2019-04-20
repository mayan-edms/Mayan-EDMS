from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured

from mayan.apps.acls.models import AccessControlList
from mayan.apps.permissions.tests.mixins import (
    PermissionTestMixin, RoleTestCaseMixin, RoleTestMixin
)
from mayan.apps.user_management.tests.mixins import UserTestCaseMixin


class ACLTestCaseMixin(RoleTestCaseMixin, UserTestCaseMixin):
    def setUp(self):
        super(ACLTestCaseMixin, self).setUp()
        if hasattr(self, '_test_case_user'):
            self._test_case_role.groups.add(self._test_case_group)

    def grant_access(self, obj, permission):
        if not hasattr(self, '_test_case_role'):
            raise ImproperlyConfigured(
                'Enable the creation of the test case user, group, and role '
                'in order to enable the usage of ACLs in tests.'
            )

        self._test_case_acl = AccessControlList.objects.grant(
            obj=obj, permission=permission, role=self._test_case_role
        )


class ACLTestMixin(PermissionTestMixin, RoleTestMixin):
    auto_create_test_role = True

    def _create_test_acl(self):
        self.test_acl = AccessControlList.objects.create(
            content_object=self.test_object, role=self.test_role
        )

    def setUp(self):
        super(ACLTestMixin, self).setUp()
        if self.auto_create_test_role:
            self._create_test_role()
