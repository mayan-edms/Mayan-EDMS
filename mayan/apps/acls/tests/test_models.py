from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.db import models

from mayan.apps.events.classes import EventModelRegistry
from mayan.apps.testing.tests.base import BaseTestCase

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
        EventModelRegistry.register(model=self.TestModel)
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
        EventModelRegistry.register(model=self.TestModel)
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

    def test_sub_model_with_multiple_inheritance_parent_with_common_super_parent_paths(self):
        self._create_test_permission()

        self.TestModelLevel1 = self._create_test_model(
            model_name='TestModelLevel1'
        )
        self.TestModelLevel2 = self._create_test_model(
            fields={
                'level_1': models.ForeignKey(
                    on_delete=models.CASCADE, to='TestModelLevel1'
                )
            }, model_name='TestModelLevel2'
        )
        self.TestModelLevel3 = self._create_test_model(
            fields={
                'level_2': models.ForeignKey(
                    on_delete=models.CASCADE, to='TestModelLevel2'
                )
            }, model_name='TestModelLevel3'
        )
        self.TestModelLevel4 = self._create_test_model(
            fields={
                'level_3': models.ForeignKey(
                    on_delete=models.CASCADE, to='TestModelLevel3'
                )
            }, model_name='TestModelLevel4'
        )

        ModelPermission.register(
            model=self.TestModelLevel2, permissions=(
                self.test_permission,
            )
        )

        ModelPermission.register_inheritance(
            model=self.TestModelLevel2, related='level_1',
        )
        ModelPermission.register_inheritance(
            model=self.TestModelLevel3, related='level_2__level_1',
        )
        ModelPermission.register_inheritance(
            model=self.TestModelLevel3, related='level_2',
        )
        ModelPermission.register_inheritance(
            model=self.TestModelLevel4, related='level_3',
        )

        level_1 = self.TestModelLevel1.objects.create()
        level_2 = self.TestModelLevel2.objects.create(level_1=level_1)
        level_3 = self.TestModelLevel3.objects.create(level_2=level_2)
        level_4 = self.TestModelLevel4.objects.create(level_3=level_3)

        self.grant_access(
            obj=level_2, permission=self.test_permission
        )

        queryset = AccessControlList.objects.restrict_queryset(
            permission=self.test_permission,
            queryset=self.TestModelLevel4.objects.all(),
            user=self._test_case_user
        )

        self.assertTrue(level_4 in queryset)


class GenericForeignKeyFieldModelTestCase(ACLTestMixin, BaseTestCase):
    auto_create_acl_test_object = False

    def test_generic_foreign_key_model_with_alternate_ct_and_fk(self):
        self._create_test_permission()

        self.TestModelExternal = self._create_test_model(
            model_name='TestModelExternal'
        )
        self.TestModelChild = self._create_test_model(
            fields={
                'content_type_1': models.ForeignKey(
                    on_delete=models.CASCADE, related_name='object_content_type',
                    to=ContentType
                ),
                'object_id_1': models.PositiveIntegerField(),
                'content_object_1': GenericForeignKey(
                    ct_field='content_type_1', fk_field='object_id_1',
                )
            }, model_name='TestModelChild'
        )

        ModelPermission.register(
            model=self.TestModelExternal, permissions=(
                self.test_permission,
            )
        )
        ModelPermission.register(
            model=self.TestModelChild, permissions=(
                self.test_permission,
            )
        )

        ModelPermission.register_inheritance(
            model=self.TestModelChild, related='content_object_1',
        )

        test_external_object = self.TestModelExternal.objects.create()
        test_object = self.TestModelChild.objects.create(
            content_object_1=test_external_object
        )

        self.grant_access(
            obj=test_external_object, permission=self.test_permission
        )

        queryset = AccessControlList.objects.restrict_queryset(
            queryset=self.TestModelChild.objects.all(),
            permission=self.test_permission, user=self._test_case_user
        )

        self.assertTrue(test_object in queryset)

    def test_generic_foreign_key_model_with_multiple_alternate_ct_and_fk(self):
        self._create_test_permission()

        self.TestModelExternal = self._create_test_model(
            model_name='TestModelExternal'
        )
        self.TestModelChild = self._create_test_model(
            fields={
                'content_type_1': models.ForeignKey(
                    on_delete=models.CASCADE,
                    related_name='object_content_type', to=ContentType
                ),
                'object_id_1': models.PositiveIntegerField(),
                'content_object_1': GenericForeignKey(
                    ct_field='content_type_1', fk_field='object_id_1',
                ),
                'content_type_2': models.ForeignKey(
                    blank=True, null=True, on_delete=models.CASCADE,
                    related_name='object_content_type',
                    to=ContentType
                ),
                'object_id_2': models.PositiveIntegerField(
                    blank=True, null=True
                ),
                'content_object_2': GenericForeignKey(
                    ct_field='content_type_2', fk_field='object_id_2',
                )
            }, model_name='TestModelChild'
        )

        ModelPermission.register(
            model=self.TestModelExternal, permissions=(
                self.test_permission,
            )
        )
        ModelPermission.register(
            model=self.TestModelChild, permissions=(
                self.test_permission,
            )
        )

        ModelPermission.register_inheritance(
            model=self.TestModelChild, related='content_object_1',
        )
        ModelPermission.register_inheritance(
            model=self.TestModelChild, related='content_object_2',
        )

        test_external_object = self.TestModelExternal.objects.create()
        test_object = self.TestModelChild.objects.create(
            content_object_1=test_external_object
        )

        self.grant_access(
            obj=test_external_object, permission=self.test_permission
        )

        queryset = AccessControlList.objects.restrict_queryset(
            queryset=self.TestModelChild.objects.all(),
            permission=self.test_permission, user=self._test_case_user
        )

        self.assertTrue(test_object in queryset)

    def test_generic_foreign_key_model_with_typecasting(self):
        self._create_test_permission()

        self.TestModelExternal = self._create_test_model(
            model_name='TestModelExternal'
        )
        self.TestModelChild = self._create_test_model(
            fields={
                'content_type': models.ForeignKey(
                    on_delete=models.CASCADE, related_name='object_content_type',
                    to=ContentType
                ),
                'object_id': models.CharField(max_length=255),
                'content_object': GenericForeignKey(
                    ct_field='content_type', fk_field='object_id',
                )
            }, model_name='TestModelChild'
        )

        ModelPermission.register(
            model=self.TestModelExternal, permissions=(
                self.test_permission,
            )
        )
        ModelPermission.register(
            model=self.TestModelChild, permissions=(
                self.test_permission,
            )
        )

        ModelPermission.register_inheritance(
            model=self.TestModelChild, related='content_object',
            fk_field_cast=models.CharField
        )

        test_external_object = self.TestModelExternal.objects.create()
        test_object = self.TestModelChild.objects.create(
            content_object=test_external_object
        )

        self.grant_access(
            obj=test_external_object, permission=self.test_permission
        )

        queryset = AccessControlList.objects.restrict_queryset(
            queryset=self.TestModelChild.objects.all(),
            permission=self.test_permission, user=self._test_case_user
        )

        self.assertTrue(test_object in queryset)


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
