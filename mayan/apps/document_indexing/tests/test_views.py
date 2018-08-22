from __future__ import absolute_import, unicode_literals

from documents.tests import GenericDocumentViewTestCase

from ..models import Index
from ..permissions import (
    permission_document_indexing_create, permission_document_indexing_delete,
    permission_document_indexing_edit,
    permission_document_indexing_instance_view,
    permission_document_indexing_view
)

from .literals import (
    TEST_INDEX_LABEL, TEST_INDEX_LABEL_EDITED, TEST_INDEX_SLUG,
    TEST_INDEX_TEMPLATE_LABEL_EXPRESSION
)


class IndexViewTestCase(GenericDocumentViewTestCase):
    def _request_index_create_view(self):
        return self.post(
            'indexing:index_setup_create', data={
                'label': TEST_INDEX_LABEL, 'slug': TEST_INDEX_SLUG
            }
        )

    def test_index_create_view_no_permission(self):
        self.login_user()

        response = self._request_index_create_view()
        self.assertEquals(response.status_code, 403)
        self.assertEqual(Index.objects.count(), 0)

    def test_index_create_view_with_permission(self):
        self.login_user()

        self.grant_permission(
            permission=permission_document_indexing_create
        )

        response = self._request_index_create_view()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Index.objects.count(), 1)
        self.assertEqual(Index.objects.first().label, TEST_INDEX_LABEL)

    def _request_index_delete_view(self, index):
        return self.post('indexing:index_setup_delete', args=(index.pk,))

    def test_index_delete_view_no_permission(self):
        self.login_user()

        index = Index.objects.create(
            label=TEST_INDEX_LABEL, slug=TEST_INDEX_SLUG
        )

        response = self._request_index_delete_view(index=index)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Index.objects.count(), 1)

    def test_index_delete_view_with_permission(self):
        self.login_user()

        self.role.permissions.add(
            permission_document_indexing_delete.stored_permission
        )

        index = Index.objects.create(
            label=TEST_INDEX_LABEL, slug=TEST_INDEX_SLUG
        )

        response = self._request_index_delete_view(index=index)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Index.objects.count(), 0)

    def _request_index_edit_view(self, index):
        return self.post(
            'indexing:index_setup_edit', args=(index.pk,), data={
                'label': TEST_INDEX_LABEL_EDITED, 'slug': TEST_INDEX_SLUG
            }
        )

    def test_index_edit_view_no_permission(self):
        self.login_user()

        index = Index.objects.create(
            label=TEST_INDEX_LABEL, slug=TEST_INDEX_SLUG
        )

        response = self._request_index_edit_view(index=index)
        self.assertEqual(response.status_code, 403)
        index = Index.objects.get(pk=index.pk)
        self.assertEqual(index.label, TEST_INDEX_LABEL)

    def test_index_edit_view_with_access(self):
        self.login_user()

        index = Index.objects.create(
            label=TEST_INDEX_LABEL, slug=TEST_INDEX_SLUG
        )

        self.grant_access(
            permission=permission_document_indexing_edit,
            obj=index
        )

        response = self._request_index_edit_view(index=index)
        self.assertEqual(response.status_code, 302)
        index.refresh_from_db()
        self.assertEqual(index.label, TEST_INDEX_LABEL_EDITED)

    def create_test_index(self):
        # Create empty index
        index = Index.objects.create(label=TEST_INDEX_LABEL)

        # Add our document type to the new index
        index.document_types.add(self.document_type)

        # Create simple index template
        root = index.template_root
        index.node_templates.create(
            parent=root, expression=TEST_INDEX_TEMPLATE_LABEL_EXPRESSION,
            link_documents=True
        )

        # Rebuild indexes
        Index.objects.rebuild()

        return index

    def _request_index_instance_node_view(self, index_instance_node):
        return self.get(
            'indexing:index_instance_node_view', args=(index_instance_node.pk,)
        )

    def test_index_instance_node_view_no_permission(self):
        index = self.create_test_index()

        self.login_user()

        response = self._request_index_instance_node_view(
            index_instance_node=index.instance_root
        )

        self.assertEqual(response.status_code, 403)

    def test_index_instance_node_view_with_access(self):
        index = self.create_test_index()

        self.login_user()

        self.grant_access(
            permission=permission_document_indexing_instance_view,
            obj=index
        )

        response = self._request_index_instance_node_view(
            index_instance_node=index.instance_root
        )

        self.assertContains(response, text=TEST_INDEX_LABEL, status_code=200)
