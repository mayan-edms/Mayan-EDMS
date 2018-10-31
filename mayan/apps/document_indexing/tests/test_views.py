from __future__ import absolute_import, unicode_literals

from documents.tests import GenericDocumentViewTestCase

from ..models import Index
from ..permissions import (
    permission_document_indexing_create, permission_document_indexing_delete,
    permission_document_indexing_edit,
    permission_document_indexing_instance_view,
    permission_document_indexing_rebuild
)

from .literals import (
    TEST_INDEX_LABEL, TEST_INDEX_LABEL_EDITED, TEST_INDEX_SLUG,
    TEST_INDEX_TEMPLATE_DOCUMENT_LABEL_EXPRESSION
)


class IndexViewTestCase(GenericDocumentViewTestCase):
    def setUp(self):
        super(IndexViewTestCase, self).setUp()
        self.login_user()

    def _request_index_create_view(self):
        return self.post(
            'indexing:index_setup_create', data={
                'label': TEST_INDEX_LABEL, 'slug': TEST_INDEX_SLUG
            }
        )

    def test_index_create_view_no_permission(self):
        response = self._request_index_create_view()
        self.assertEquals(response.status_code, 403)
        self.assertEqual(Index.objects.count(), 0)

    def test_index_create_view_with_permission(self):
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
        index = Index.objects.create(
            label=TEST_INDEX_LABEL, slug=TEST_INDEX_SLUG
        )

        response = self._request_index_delete_view(index=index)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Index.objects.count(), 1)

    def test_index_delete_view_with_permission(self):
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
        index = Index.objects.create(
            label=TEST_INDEX_LABEL, slug=TEST_INDEX_SLUG
        )

        response = self._request_index_edit_view(index=index)
        self.assertEqual(response.status_code, 403)
        index = Index.objects.get(pk=index.pk)
        self.assertEqual(index.label, TEST_INDEX_LABEL)

    def test_index_edit_view_with_access(self):
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

    def _create_index(self, rebuild=True):
        # Create empty index
        self.index = Index.objects.create(label=TEST_INDEX_LABEL)

        # Add our document type to the new index
        self.index.document_types.add(self.document_type)

        # Create simple index template
        root = self.index.template_root
        self.index.node_templates.create(
            parent=root, expression=TEST_INDEX_TEMPLATE_DOCUMENT_LABEL_EXPRESSION,
            link_documents=True
        )

        # Rebuild indexes
        if rebuild:
            Index.objects.rebuild()

    def _request_index_instance_node_view(self, index_instance_node):
        return self.get(
            'indexing:index_instance_node_view', args=(index_instance_node.pk,)
        )

    def test_index_instance_node_view_no_permission(self):
        self._create_index()

        response = self._request_index_instance_node_view(
            index_instance_node=self.index.instance_root
        )

        self.assertEqual(response.status_code, 403)

    def test_index_instance_node_view_with_access(self):
        self._create_index()

        self.grant_access(
            permission=permission_document_indexing_instance_view,
            obj=self.index
        )

        response = self._request_index_instance_node_view(
            index_instance_node=self.index.instance_root
        )

        self.assertContains(response, text=TEST_INDEX_LABEL, status_code=200)

    def _request_index_rebuild_get_view(self):
        return self.get(
            viewname='indexing:rebuild_index_instances',
        )

    def _request_index_rebuild_post_view(self):
        return self.post(
            viewname='indexing:rebuild_index_instances', data={
                'indexes': self.index.pk
            }
        )

    def test_index_rebuild_no_permission(self):
        self._create_index(rebuild=False)

        response = self._request_index_rebuild_get_view()
        self.assertNotContains(response=response, text=self.index.label, status_code=200)

        response = self._request_index_rebuild_post_view()
        # No error since we just don't see the index
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.index.instance_root.get_children_count(), 0
        )

    def test_index_rebuild_with_access(self):
        self._create_index(rebuild=False)

        self.grant_access(
            permission=permission_document_indexing_rebuild, obj=self.index
        )

        response = self._request_index_rebuild_get_view()
        self.assertContains(response=response, text=self.index.label, status_code=200)

        response = self._request_index_rebuild_post_view()
        self.assertEqual(response.status_code, 302)

        # An instance root exists
        self.assertTrue(self.index.instance_root.pk)
