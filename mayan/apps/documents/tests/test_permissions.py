from mayan.apps.acls.classes import ModelPermission
from mayan.apps.acls.permissions import permission_acl_edit
from mayan.apps.acls.tests.mixins import (
    ACLTestMixin, AccessControlListViewTestMixin
)
from mayan.apps.testing.tests.base import BaseTestCase

from ..models import DocumentType
from ..permissions import permission_document_view

from .base import GenericDocumentViewTestCase


class DocumentTypeACLPermissionsTestCase(BaseTestCase):
    def test_document_type_permission_test(self):
        result = ModelPermission.get_for_class(klass=DocumentType)
        self.assertTrue(permission_document_view in result)


class DocumentTypeACLPermissionsViewTestCase(
    ACLTestMixin, AccessControlListViewTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def test_document_type_acl_permission_view_with_access(self):
        self.test_object = self.test_document_type
        self._create_test_acl()
        self.grant_access(
            obj=self.test_object, permission=permission_acl_edit
        )

        response = self._request_test_acl_permission_list_get_view()
        self.assertContains(
            response=response, text=permission_document_view.label,
            status_code=200
        )
