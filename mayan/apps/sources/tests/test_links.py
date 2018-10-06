from __future__ import unicode_literals

from documents.tests import GenericDocumentViewTestCase
from documents.permissions import permission_document_create

from ..links import link_document_create_multiple


class SourcesLinksTestCase(GenericDocumentViewTestCase):
    def setUp(self):
        super(SourcesLinksTestCase, self).setUp()
        self.login_user()

    def _get_document_create_link(self):
        self.add_test_view(test_object=self.document)
        context = self.get_test_view()
        context['user'] = self.user
        return link_document_create_multiple.resolve(context=context)

    def test_document_create_link_no_access(self):
        resolved_link = self._get_document_create_link()
        self.assertEqual(resolved_link, None)

    def test_document_create_link_with_access(self):
        self.grant_access(
            permission=permission_document_create, obj=self.document_type
        )
        resolved_link = self._get_document_create_link()
        self.assertNotEqual(resolved_link, None)
