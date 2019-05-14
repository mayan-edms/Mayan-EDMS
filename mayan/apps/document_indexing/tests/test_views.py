from __future__ import absolute_import, unicode_literals

from mayan.apps.documents.tests import GenericDocumentViewTestCase

from ..models import Index
from ..permissions import (
    permission_document_indexing_create, permission_document_indexing_delete,
    permission_document_indexing_edit,
    permission_document_indexing_instance_view,
    permission_document_indexing_rebuild
)

from .literals import TEST_INDEX_LABEL, TEST_INDEX_LABEL_EDITED
from .mixins import IndexTestMixin, IndexViewTestMixin


class IndexViewTestCase(IndexTestMixin, IndexViewTestMixin, GenericDocumentViewTestCase):
    def test_index_create_view_no_permission(self):
        response = self._request_test_index_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(Index.objects.count(), 0)

    def test_index_create_view_with_permission(self):
        self.grant_permission(
            permission=permission_document_indexing_create
        )

        response = self._request_test_index_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Index.objects.count(), 1)
        self.assertEqual(Index.objects.first().label, TEST_INDEX_LABEL)

    def test_index_delete_view_no_permission(self):
        self._create_test_index()

        response = self._request_test_index_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(Index.objects.count(), 1)

    def test_index_delete_view_with_permission(self):
        self._create_test_index()

        self.grant_permission(permission=permission_document_indexing_delete)

        response = self._request_test_index_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(Index.objects.count(), 0)

    def test_index_edit_view_no_permission(self):
        self._create_test_index()

        response = self._request_test_index_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_index.refresh_from_db()
        self.assertEqual(self.test_index.label, TEST_INDEX_LABEL)

    def test_index_edit_view_with_access(self):
        self._create_test_index()

        self.grant_access(
            obj=self.test_index, permission=permission_document_indexing_edit
        )

        response = self._request_test_index_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_index.refresh_from_db()
        self.assertEqual(self.test_index.label, TEST_INDEX_LABEL_EDITED)

    def _request_index_instance_node_view(self, index_instance_node):
        return self.get(
            viewname='indexing:index_instance_node_view', kwargs={
                'pk': index_instance_node.pk
            }
        )

    def test_index_instance_node_view_no_permission(self):
        self._create_test_index()

        response = self._request_index_instance_node_view(
            index_instance_node=self.test_index.instance_root
        )
        self.assertEqual(response.status_code, 403)

    def test_index_instance_node_view_with_access(self):
        self._create_test_index()

        self.grant_access(
            obj=self.test_index,
            permission=permission_document_indexing_instance_view
        )

        response = self._request_index_instance_node_view(
            index_instance_node=self.test_index.instance_root
        )
        self.assertContains(response, text=TEST_INDEX_LABEL, status_code=200)

    def _request_index_rebuild_get_view(self):
        return self.get(
            viewname='indexing:rebuild_index_instances',
        )

    def _request_index_rebuild_post_view(self):
        return self.post(
            viewname='indexing:rebuild_index_instances', data={
                'index_templates': self.test_index.pk
            }
        )

    def test_index_rebuild_no_permission(self):
        self._create_test_index(rebuild=False)

        response = self._request_index_rebuild_get_view()
        self.assertNotContains(
            response=response, text=self.test_index.label, status_code=200
        )

        response = self._request_index_rebuild_post_view()
        # No error since we just don't see the index
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.test_index.instance_root.get_children_count(), 0
        )

    def test_index_rebuild_with_access(self):
        self._create_test_index(rebuild=False)

        self.grant_access(
            obj=self.test_index,
            permission=permission_document_indexing_rebuild
        )

        response = self._request_index_rebuild_get_view()
        self.assertContains(
            response=response, text=self.test_index.label, status_code=200
        )

        response = self._request_index_rebuild_post_view()
        self.assertEqual(response.status_code, 302)

        # An instance root exists
        self.assertTrue(self.test_index.instance_root.pk)
