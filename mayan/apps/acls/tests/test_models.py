from __future__ import absolute_import, unicode_literals

from django.core.exceptions import PermissionDenied

from mayan.apps.common.tests import BaseTestCase
from mayan.apps.documents.models import Document, DocumentType
from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.tests import (
    TEST_SMALL_DOCUMENT_PATH, TEST_DOCUMENT_TYPE_LABEL,
    TEST_DOCUMENT_TYPE_2_LABEL
)

from ..models import AccessControlList

from .mixins import ACLTestMixin


class PermissionTestCase(ACLTestMixin, BaseTestCase):
    def setUp(self):
        super(PermissionTestCase, self).setUp()
        self.document_type_1 = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_LABEL
        )

        self.document_type_2 = DocumentType.objects.create(
            label=TEST_DOCUMENT_TYPE_2_LABEL
        )

        with open(TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            self.document_1 = self.document_type_1.new_document(
                file_object=file_object
            )

        with open(TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            self.document_2 = self.document_type_1.new_document(
                file_object=file_object
            )

        with open(TEST_SMALL_DOCUMENT_PATH, mode='rb') as file_object:
            self.document_3 = self.document_type_2.new_document(
                file_object=file_object
            )

    def tearDown(self):
        for document_type in DocumentType.objects.all():
            document_type.delete()
        super(PermissionTestCase, self).tearDown()

    def test_check_access_without_permissions(self):
        with self.assertRaises(PermissionDenied):
            AccessControlList.objects.check_access(
                permissions=(permission_document_view,),
                user=self._test_case_user, obj=self.document_1
            )

    def test_filtering_without_permissions(self):
        self.assertQuerysetEqual(
            AccessControlList.objects.filter_by_access(
                permission=permission_document_view, user=self._test_case_user,
                queryset=Document.objects.all()
            ), []
        )

    def test_check_access_with_acl(self):
        self.grant_access(
            obj=self.document_1, permission=permission_document_view
        )

        try:
            AccessControlList.objects.check_access(
                obj=self.document_1, permissions=(permission_document_view,),
                user=self._test_case_user,
            )
        except PermissionDenied:
            self.fail('PermissionDenied exception was not expected.')

    def test_filtering_with_permissions(self):
        self.grant_access(
            obj=self.document_1, permission=permission_document_view
        )

        self.assertQuerysetEqual(
            AccessControlList.objects.filter_by_access(
                permission=permission_document_view,
                queryset=Document.objects.all(), user=self._test_case_user
            ), (repr(self.document_1),)
        )

    def test_check_access_with_inherited_acl(self):
        self.grant_access(
            obj=self.document_type_1, permission=permission_document_view
        )

        try:
            AccessControlList.objects.check_access(
                obj=self.document_1, permissions=(permission_document_view,),
                user=self._test_case_user
            )
        except PermissionDenied:
            self.fail('PermissionDenied exception was not expected.')

    def test_check_access_with_inherited_acl_and_local_acl(self):
        self.grant_access(
            obj=self.document_type_1, permission=permission_document_view
        )
        self.grant_access(
            obj=self.document_3, permission=permission_document_view
        )

        try:
            AccessControlList.objects.check_access(
                obj=self.document_3, permissions=(permission_document_view,),
                user=self._test_case_user
            )
        except PermissionDenied:
            self.fail('PermissionDenied exception was not expected.')

    def test_filtering_with_inherited_permissions(self):
        self.grant_access(
            obj=self.document_type_1, permission=permission_document_view
        )

        result = AccessControlList.objects.filter_by_access(
            permission=permission_document_view,
            queryset=Document.objects.all(), user=self._test_case_user
        )

        # Since document_1 and document_2 are of document_type_1
        # they are the only ones that should be returned

        self.assertTrue(self.document_1 in result)
        self.assertTrue(self.document_2 in result)
        self.assertTrue(self.document_3 not in result)

    def test_filtering_with_inherited_permissions_and_local_acl(self):
        self.grant_permission(permission=permission_document_view)
        self.grant_access(
            obj=self.document_type_1, permission=permission_document_view
        )
        self.grant_access(
            obj=self.document_3, permission=permission_document_view
        )

        result = AccessControlList.objects.filter_by_access(
            permission=permission_document_view,
            queryset=Document.objects.all(), user=self._test_case_user,
        )
        self.assertTrue(self.document_1 in result)
        self.assertTrue(self.document_2 in result)
        self.assertTrue(self.document_3 in result)
