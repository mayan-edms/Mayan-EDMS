from __future__ import unicode_literals

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.acls.permissions import permission_acl_edit
from mayan.apps.acls.tests.mixins import ACLTestMixin
from mayan.apps.common.tests.base import BaseTestCase

from ..models import DocumentType
from ..permissions import permission_document_view

from .base import GenericDocumentViewTestCase


class DocumentTypeACLPermissionsTestCase(BaseTestCase):
    def test_document_type_permission_test(self):
        result = ModelPermission.get_for_class(klass=DocumentType)
        self.assertTrue(permission_document_view in result)


class DocumentTypeACLPermissionsViewTestCase(
    ACLTestMixin, GenericDocumentViewTestCase
):
    auto_upload_document = False

    def test_document_type_acl_permission_view_test(self):
        self.test_object = self.test_document_type
        self._create_test_acl()
        self.grant_access(
            obj=self.test_object, permission=permission_acl_edit
        )

        response = self.get(
            viewname='acls:acl_permissions', kwargs={'pk': self.test_acl.pk}
        )
        self.assertContains(
            response=response, text=permission_document_view.label,
            status_code=200
        )
