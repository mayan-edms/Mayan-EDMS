from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured

from mayan.apps.common.tests.mixins import TestModelTestMixin
from mayan.apps.permissions.tests.mixins import (
    PermissionTestMixin, RoleTestCaseMixin, RoleTestMixin
)
from mayan.apps.user_management.tests.mixins import UserTestCaseMixin

from ..classes import ModelPermission
from ..models import AccessControlList
from ..permissions import permission_acl_edit, permission_acl_view


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


class ACLTestMixin(PermissionTestMixin, RoleTestMixin, TestModelTestMixin):
    auto_create_test_role = True
    auto_create_test_object = False

    def setUp(self):
        super(ACLTestMixin, self).setUp()
        if self.auto_create_test_role:
            self._create_test_role()

        if self.auto_create_test_object:
            self._setup_test_object()

    def tearDown(self):
        # Deregister the permissions of the ephimeral test models
        # this avoids their Content Type from being looked up
        # in subsequent tests where they don't exists due to the database
        # transaction rollback.
        for model in self._test_models:
            ModelPermission.deregister(model=model)
            self._test_models.remove(model)

        super(ACLTestMixin, self).tearDown()

    def _create_test_acl(self):
        self.test_acl = AccessControlList.objects.create(
            content_object=self.test_object, role=self.test_role
        )

    def _inject_test_object_content_type(self):
        self.test_object_content_type = ContentType.objects.get_for_model(
            model=self.test_object
        )

        self.test_content_object_view_kwargs = {
            'app_label': self.test_object_content_type.app_label,
            'model': self.test_object_content_type.model,
            'object_id': self.test_object.pk
        }

    def _setup_test_object(self, register_model_permissions=True):
        self._create_test_model()
        self._create_test_object()
        if register_model_permissions:
            ModelPermission.register(
                model=self.test_object._meta.model, permissions=(
                    permission_acl_edit, permission_acl_view,
                )
            )

        self._create_test_permission()

        if register_model_permissions:
            ModelPermission.register(
                model=self.test_object._meta.model, permissions=(
                    self.test_permission,
                )
            )

        self._inject_test_object_content_type()
