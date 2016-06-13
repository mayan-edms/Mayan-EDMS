from __future__ import absolute_import, unicode_literals

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.test import TestCase, override_settings

from documents.models import Document, DocumentType
from documents.permissions import permission_document_view
from documents.tests import TEST_SMALL_DOCUMENT_PATH, TEST_DOCUMENT_TYPE
from organizations.tests.base import OrganizationTestCase
from permissions.classes import Permission
from permissions.models import Role
from permissions.tests.literals import TEST_ROLE_LABEL
from user_management.models import MayanGroup
from user_management.tests.literals import TEST_USER_USERNAME, TEST_GROUP

from ..models import AccessControlList

TEST_DOCUMENT_TYPE_2 = 'test document type 2'


@override_settings(OCR_AUTO_OCR=False)
class PermissionTestCase(OrganizationTestCase):
    def setUp(self):
        super(PermissionTestCase, self).setUp()

        self.document_type_1 = DocumentType.on_organization.create(
            label=TEST_DOCUMENT_TYPE
        )

        self.document_type_2 = DocumentType.on_organization.create(
            label=TEST_DOCUMENT_TYPE_2
        )

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document_1 = self.document_type_1.new_document(
                file_object=file_object
            )

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document_2 = self.document_type_1.new_document(
                file_object=file_object
            )

        with open(TEST_SMALL_DOCUMENT_PATH) as file_object:
            self.document_3 = self.document_type_2.new_document(
                file_object=file_object
            )

        self.user = get_user_model().on_organization.create(
            username=TEST_USER_USERNAME
        )
        self.group = MayanGroup.on_organization.create(name=TEST_GROUP)
        self.role = Role.on_organization.create(label=TEST_ROLE_LABEL)

        self.group.users.add(self.user)
        self.role.organization_groups.add(self.group)

        Permission.invalidate_cache()

    def tearDown(self):
        for document_type in DocumentType.on_organization.all():
            document_type.delete()

        super(PermissionTestCase, self).tearDown()

    def test_check_access_without_permissions(self):
        with self.assertRaises(PermissionDenied):
            AccessControlList.objects.check_access(
                permissions=(permission_document_view,),
                user=self.user, obj=self.document_1
            )

    def test_filtering_without_permissions(self):
        self.assertQuerysetEqual(
            AccessControlList.objects.filter_by_access(
                permission=permission_document_view, user=self.user,
                queryset=Document.objects.all()
            ), []
        )

    def test_check_access_with_acl(self):
        acl = AccessControlList.on_organization.create(
            content_object=self.document_1, role=self.role
        )
        acl.permissions.add(permission_document_view.stored_permission)

        try:
            AccessControlList.objects.check_access(
                permissions=(permission_document_view,), user=self.user,
                obj=self.document_1
            )
        except PermissionDenied:
            self.fail('PermissionDenied exception was not expected.')

    def test_filtering_with_permissions(self):
        self.role.permissions.add(permission_document_view.stored_permission)

        acl = AccessControlList.on_organization.create(
            content_object=self.document_1, role=self.role
        )
        acl.permissions.add(permission_document_view.stored_permission)

        self.assertQuerysetEqual(
            AccessControlList.objects.filter_by_access(
                permission=permission_document_view, user=self.user,
                queryset=Document.objects.all()
            ), (repr(self.document_1),)
        )

    def test_check_access_with_inherited_acl(self):
        acl = AccessControlList.on_organization.create(
            content_object=self.document_type_1, role=self.role
        )
        acl.permissions.add(permission_document_view.stored_permission)

        try:
            AccessControlList.objects.check_access(
                permissions=(permission_document_view,), user=self.user,
                obj=self.document_1
            )
        except PermissionDenied:
            self.fail('PermissionDenied exception was not expected.')

    def test_check_access_with_inherited_acl_and_local_acl(self):
        acl = AccessControlList.on_organization.create(
            content_object=self.document_type_1, role=self.role
        )
        acl.permissions.add(permission_document_view.stored_permission)

        acl = AccessControlList.on_organization.create(
            content_object=self.document_3, role=self.role
        )
        acl.permissions.add(permission_document_view.stored_permission)

        try:
            AccessControlList.objects.check_access(
                permissions=(permission_document_view,), user=self.user,
                obj=self.document_3
            )
        except PermissionDenied:
            self.fail('PermissionDenied exception was not expected.')

    def test_filtering_with_inherited_permissions(self):
        self.role.permissions.add(permission_document_view.stored_permission)

        acl = AccessControlList.on_organization.create(
            content_object=self.document_type_1, role=self.role
        )
        acl.permissions.add(permission_document_view.stored_permission)

        result = AccessControlList.objects.filter_by_access(
            permission=permission_document_view, user=self.user,
            queryset=Document.objects.all()
        )
        self.assertTrue(self.document_1 in result)
        self.assertTrue(self.document_2 in result)
        self.assertTrue(self.document_3 not in result)

    def test_filtering_with_inherited_permissions_and_local_acl(self):
        self.role.permissions.add(permission_document_view.stored_permission)

        acl = AccessControlList.on_organization.create(
            content_object=self.document_type_1, role=self.role
        )
        acl.permissions.add(permission_document_view.stored_permission)

        acl = AccessControlList.on_organization.create(
            content_object=self.document_3, role=self.role
        )
        acl.permissions.add(permission_document_view.stored_permission)

        result = AccessControlList.objects.filter_by_access(
            permission=permission_document_view, user=self.user,
            queryset=Document.objects.all()
        )
        self.assertTrue(self.document_1 in result)
        self.assertTrue(self.document_2 in result)
        self.assertTrue(self.document_3 in result)
