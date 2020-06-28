from django.core.exceptions import PermissionDenied
from django.db import models

from mayan.apps.tests.tests.base import BaseTestCase

from ..classes import ModelPermission
from ..models import AccessControlList

from .mixins import ACLTestMixin


class PermissionTestCase(ACLTestMixin, BaseTestCase):
    auto_create_acl_test_object = False

    def test_check_access_without_permissions(self):
        self._create_acl_test_object()

        with self.assertRaises(expected_exception=PermissionDenied):
            AccessControlList.objects.check_access(
                obj=self.test_object,
                permissions=(self.test_permission,),
                user=self._test_case_user,
            )

    def test_filtering_without_permissions(self):
        self._create_acl_test_object()

        self.assertEqual(
            AccessControlList.objects.restrict_queryset(
                permission=self.test_permission,
                queryset=self.test_object._meta.model._default_manager.all(),
                user=self._test_case_user
            ).count(), 0
        )

    def test_check_access_with_acl(self):
        self._create_acl_test_object()

        self.grant_access(
            obj=self.test_object, permission=self.test_permission
        )

        try:
            AccessControlList.objects.check_access(
                obj=self.test_object, permissions=(self.test_permission,),
                user=self._test_case_user,
            )
        except PermissionDenied:
            self.fail('PermissionDenied exception was not expected.')

    def test_filtering_with_permissions(self):
        self._create_acl_test_object()

        self.grant_access(
            obj=self.test_object, permission=self.test_permission
        )

        self.assertTrue(
            self.test_object in AccessControlList.objects.restrict_queryset(
                permission=self.test_permission,
                queryset=self.test_object._meta.model._default_manager.all(),
                user=self._test_case_user
            )
        )

    def _setup_child_parent_test_objects(self):
        self._create_test_permission()
        self.TestModelParent = self._create_test_model(
            model_name='TestModelParent'
        )
        self.TestModelChild = self._create_test_model(
            fields={
                'parent': models.ForeignKey(
                    on_delete=models.CASCADE, related_name='children',
                    to='TestModelParent',
                )
            }, model_name='TestModelChild'
        )

        ModelPermission.register(
            model=self.TestModelParent, permissions=(
                self.test_permission,
            )
        )
        ModelPermission.register(
            model=self.TestModelChild, permissions=(
                self.test_permission,
            )
        )
        ModelPermission.register_inheritance(
            model=self.TestModelChild, related='parent',
        )

        self.test_object_parent = self.TestModelParent.objects.create()
        self.test_object_child = self.TestModelChild.objects.create(
            parent=self.test_object_parent
        )

    def test_check_access_with_inherited_acl(self):
        self._setup_child_parent_test_objects()

        self.grant_access(
            obj=self.test_object_parent, permission=self.test_permission
        )

        try:
            AccessControlList.objects.check_access(
                obj=self.test_object_child,
                permissions=(self.test_permission,),
                user=self._test_case_user
            )
        except PermissionDenied:
            self.fail('PermissionDenied exception was not expected.')

    def test_check_access_with_inherited_acl_and_local_acl(self):
        self._setup_child_parent_test_objects()

        self.grant_access(
            obj=self.test_object_parent, permission=self.test_permission
        )
        self.grant_access(
            obj=self.test_object_child, permission=self.test_permission
        )

        try:
            AccessControlList.objects.check_access(
                obj=self.test_object_child,
                permissions=(self.test_permission,),
                user=self._test_case_user
            )
        except PermissionDenied:
            self.fail('PermissionDenied exception was not expected.')

    def test_filtering_with_inherited_permissions(self):
        self._setup_child_parent_test_objects()

        self.grant_access(
            obj=self.test_object_parent, permission=self.test_permission
        )

        result = AccessControlList.objects.restrict_queryset(
            permission=self.test_permission,
            queryset=self.test_object_child._meta.model._default_manager.all(),
            user=self._test_case_user
        )
        self.assertTrue(self.test_object_child in result)

    def test_filtering_with_inherited_permissions_and_local_acl(self):
        self._setup_child_parent_test_objects()

        self.grant_permission(permission=self.test_permission)
        self.grant_access(
            obj=self.test_object_parent, permission=self.test_permission
        )
        self.grant_access(
            obj=self.test_object_child, permission=self.test_permission
        )

        result = AccessControlList.objects.restrict_queryset(
            permission=self.test_permission,
            queryset=self.test_object_child._meta.model._default_manager.all(),
            user=self._test_case_user,
        )
        self.assertTrue(self.test_object_child in result)

    def test_method_get_absolute_url(self):
        self._create_acl_test_object()
        self._create_test_acl()

        self.assertTrue(self.test_acl.get_absolute_url())


class InheritedPermissionTestCase(ACLTestMixin, BaseTestCase):
    def test_retrieve_inherited_role_permission_not_model_applicable(self):
        self.TestModel = self._create_test_model()
        self.test_object = self.TestModel.objects.create()
        self._create_test_acl()
        self._create_test_permission()

        self.test_role.grant(permission=self.test_permission)

        queryset = AccessControlList.objects.get_inherited_permissions(
            obj=self.test_object, role=self.test_role
        )
        self.assertTrue(
            self.test_permission.stored_permission not in queryset
        )

    def test_retrieve_inherited_role_permission_model_applicable(self):
        self.TestModel = self._create_test_model()
        self.test_object = self.TestModel.objects.create()
        self._create_test_acl()
        self._create_test_permission()

        ModelPermission.register(
            model=self.test_object._meta.model, permissions=(
                self.test_permission,
            )
        )
        self.test_role.grant(permission=self.test_permission)

        queryset = AccessControlList.objects.get_inherited_permissions(
            obj=self.test_object, role=self.test_role
        )
        self.assertTrue(self.test_permission.stored_permission in queryset)

    def test_retrieve_inherited_related_parent_child_permission(self):
        self._create_test_permission()

        self.TestModelParent = self._create_test_model(
            model_name='TestModelParent'
        )
        self.TestModelChild = self._create_test_model(
            fields={
                'parent': models.ForeignKey(
                    on_delete=models.CASCADE, related_name='children',
                    to='TestModelParent',
                )
            }, model_name='TestModelChild'
        )

        ModelPermission.register(
            model=self.TestModelParent, permissions=(
                self.test_permission,
            )
        )
        ModelPermission.register(
            model=self.TestModelChild, permissions=(
                self.test_permission,
            )
        )
        ModelPermission.register_inheritance(
            model=self.TestModelChild, related='parent',
        )

        parent = self.TestModelParent.objects.create()
        child = self.TestModelChild.objects.create(parent=parent)

        AccessControlList.objects.grant(
            obj=parent, permission=self.test_permission, role=self.test_role
        )
        queryset = AccessControlList.objects.get_inherited_permissions(
            obj=child, role=self.test_role
        )

        self.assertTrue(self.test_permission.stored_permission in queryset)

    def test_retrieve_inherited_related_grandparent_parent_child_permission(
        self
    ):
        self._create_test_permission()

        self.TestModelGrandParent = self._create_test_model(
            model_name='TestModelGrandParent'
        )
        self.TestModelParent = self._create_test_model(
            fields={
                'parent': models.ForeignKey(
                    on_delete=models.CASCADE, related_name='children',
                    to='TestModelGrandParent',
                )
            }, model_name='TestModelParent'
        )
        self.TestModelChild = self._create_test_model(
            fields={
                'parent': models.ForeignKey(
                    on_delete=models.CASCADE, related_name='children',
                    to='TestModelParent',
                )
            }, model_name='TestModelChild'
        )

        ModelPermission.register(
            model=self.TestModelGrandParent, permissions=(
                self.test_permission,
            )
        )
        ModelPermission.register(
            model=self.TestModelParent, permissions=(
                self.test_permission,
            )
        )
        ModelPermission.register(
            model=self.TestModelChild, permissions=(
                self.test_permission,
            )
        )
        ModelPermission.register_inheritance(
            model=self.TestModelChild, related='parent',
        )
        ModelPermission.register_inheritance(
            model=self.TestModelParent, related='parent',
        )

        grandparent = self.TestModelGrandParent.objects.create()
        parent = self.TestModelParent.objects.create(parent=grandparent)
        child = self.TestModelChild.objects.create(parent=parent)

        AccessControlList.objects.grant(
            obj=grandparent, permission=self.test_permission,
            role=self.test_role
        )

        queryset = AccessControlList.objects.get_inherited_permissions(
            obj=child, role=self.test_role
        )

        self.assertTrue(self.test_permission.stored_permission in queryset)


class ProxyModelPermissionTestCase(ACLTestMixin, BaseTestCase):
    def test_proxy_model_filtering_no_permission(self):
        self._create_acl_test_object_base()
        self._create_acl_test_object_proxy()

        proxy_object = self.TestModelProxy.objects.get(pk=self.test_object.pk)

        self.assertFalse(
            proxy_object in AccessControlList.objects.restrict_queryset(
                permission=self.test_permission,
                queryset=self.TestModelProxy.objects.all(),
                user=self._test_case_user
            )
        )

    def test_proxy_model_filtering_with_access(self):
        self._create_acl_test_object_base()
        self._create_acl_test_object_proxy()

        self.grant_access(
            obj=self.test_object, permission=self.test_permission
        )

        proxy_object = self.TestModelProxy.objects.get(pk=self.test_object.pk)

        self.assertTrue(
            proxy_object in AccessControlList.objects.restrict_queryset(
                permission=self.test_permission,
                queryset=self.TestModelProxy.objects.all(),
                user=self._test_case_user
            )
        )

    def test_proxy_model_inheritance_with_access(self):
        self._create_test_permission()

        self.TestModelParent = self._create_test_model(
            model_name='TestModelParent'
        )
        self.TestModelChild = self._create_test_model(
            fields={
                'parent': models.ForeignKey(
                    on_delete=models.CASCADE, related_name='children',
                    to='TestModelParent',
                )
            }, model_name='TestModelChild'
        )
        self.TestModelProxy = self._create_test_model(
            base_class=self.TestModelChild, model_name='TestModelProxy',
            options={
                'proxy': True
            }
        )

        ModelPermission.register(
            model=self.TestModelParent, permissions=(
                self.test_permission,
            )
        )
        ModelPermission.register_inheritance(
            model=self.TestModelChild, related='parent',
        )

        parent = self.TestModelParent.objects.create()
        child = self.TestModelChild.objects.create(parent=parent)

        self.grant_access(
            obj=parent, permission=self.test_permission
        )

        proxy_object = self.TestModelProxy.objects.get(pk=child.pk)

        self.assertTrue(
            proxy_object in AccessControlList.objects.restrict_queryset(
                permission=self.test_permission,
                queryset=self.TestModelProxy.objects.all(),
                user=self._test_case_user
            )
        )
