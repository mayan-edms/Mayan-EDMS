from __future__ import unicode_literals

from mayan.apps.documents.tests import GenericDocumentViewTestCase
from mayan.apps.documents.permissions import permission_document_create

from ..links import link_document_create_multiple


class SourcesLinksTestCase(GenericDocumentViewTestCase):
    def _get_document_create_link(self):
        self.add_test_view(test_object=self.test_document)
        context = self.get_test_view()
        context['user'] = self._test_case_user
        return link_document_create_multiple.resolve(context=context)

    def test_document_create_link_no_access(self):
        resolved_link = self._get_document_create_link()
        self.assertEqual(resolved_link, None)

    def test_document_create_link_with_access(self):
        self.grant_access(
            obj=self.test_document_type, permission=permission_document_create
        )
        resolved_link = self._get_document_create_link()
        self.assertNotEqual(resolved_link, None)
