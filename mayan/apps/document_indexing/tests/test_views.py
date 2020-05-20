from mayan.apps.documents.tests.base import (
    GenericDocumentViewTestCase, GenericViewTestCase
)

from ..models import Index, IndexInstanceNode
from ..permissions import (
    permission_document_indexing_create, permission_document_indexing_delete,
    permission_document_indexing_edit,
    permission_document_indexing_instance_view,
    permission_document_indexing_rebuild
)

from .literals import TEST_INDEX_LABEL, TEST_INDEX_LABEL_EDITED
from .mixins import (
    IndexInstaceViewTestMixin, IndexTemplateNodeViewTestMixin,
    IndexTestMixin, IndexToolsViewTestMixin, IndexViewTestMixin
)


class IndexViewTestCase(
    IndexTestMixin, IndexViewTestMixin, GenericViewTestCase
):
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

    def test_index_document_types_view_no_permission(self):
        self._create_test_index()

        response = self._request_test_index_document_type_view()
        self.assertEqual(response.status_code, 404)

    def test_index_document_types_view_with_access(self):
        self._create_test_index()
        self.grant_access(
            obj=self.test_index, permission=permission_document_indexing_edit
        )

        response = self._request_test_index_document_type_view()
        self.assertEqual(response.status_code, 200)

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


class IndexInstaceViewTestCase(
    IndexTestMixin, IndexViewTestMixin, IndexInstaceViewTestMixin,
    GenericDocumentViewTestCase
):
    def test_index_rebuild_view_no_permission(self):
        self._upload_test_document()
        self._create_test_index()
        self._create_test_index_template_node()

        response = self._request_test_index_rebuild_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(IndexInstanceNode.objects.count(), 1)
        self.assertEqual(IndexInstanceNode.objects.first().parent, None)

    def test_index_rebuild_view_with_access(self):
        self._upload_test_document()
        self._create_test_index()
        self._create_test_index_template_node()

        self.grant_access(
            obj=self.test_index,
            permission=permission_document_indexing_rebuild
        )

        response = self._request_test_index_rebuild_view()
        self.assertEqual(response.status_code, 302)

        self.assertNotEqual(IndexInstanceNode.objects.count(), 0)

    def test_index_instance_node_view_no_permission(self):
        self._create_test_index()

        response = self._request_test_index_instance_node_view(
            index_instance_node=self.test_index.instance_root
        )
        self.assertEqual(response.status_code, 403)

    def test_index_instance_node_view_with_access(self):
        self._create_test_index()

        self.grant_access(
            obj=self.test_index,
            permission=permission_document_indexing_instance_view
        )

        response = self._request_test_index_instance_node_view(
            index_instance_node=self.test_index.instance_root
        )
        self.assertContains(response, text=TEST_INDEX_LABEL, status_code=200)


class IndexTemplateNodeViewTestCase(
    IndexTestMixin, IndexTemplateNodeViewTestMixin, GenericViewTestCase
):
    def test_index_template_node_create_view_no_permission(self):
        self._create_test_index()
        node_count = self.test_index.node_templates.count()

        response = self._request_test_index_node_create_view()
        self.assertEqual(response.status_code, 403)

        self.assertEqual(
            self.test_index.node_templates.count(), node_count
        )

    def test_index_template_node_create_view_with_access(self):
        self._create_test_index()
        self.grant_access(
            obj=self.test_index, permission=permission_document_indexing_edit
        )
        node_count = self.test_index.node_templates.count()

        response = self._request_test_index_node_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_index.node_templates.count(), node_count + 1
        )

    def test_index_template_node_delete_view_no_permission(self):
        self._create_test_index()
        self._create_test_index_template_node()
        node_count = self.test_index.node_templates.count()

        response = self._request_test_index_node_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(
            self.test_index.node_templates.count(), node_count
        )

    def test_index_template_node_delete_view_with_access(self):
        self._create_test_index()
        self._create_test_index_template_node()
        self.grant_access(
            obj=self.test_index, permission=permission_document_indexing_edit
        )
        node_count = self.test_index.node_templates.count()

        response = self._request_test_index_node_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_index.node_templates.count(), node_count - 1
        )

    def test_index_template_node_edit_view_no_permission(self):
        self._create_test_index()
        self._create_test_index_template_node()
        node_expression = self.test_index_template_node.expression

        response = self._request_test_index_node_edit_view()
        self.assertEqual(response.status_code, 404)

        self.test_index_template_node.refresh_from_db()
        self.assertEqual(
            self.test_index_template_node.expression, node_expression
        )

    def test_index_template_node_edit_view_with_access(self):
        self._create_test_index()
        self._create_test_index_template_node()
        self.grant_access(
            obj=self.test_index, permission=permission_document_indexing_edit
        )
        node_expression = self.test_index_template_node.expression

        response = self._request_test_index_node_edit_view()
        self.assertEqual(response.status_code, 302)

        self.test_index_template_node.refresh_from_db()
        self.assertNotEqual(
            self.test_index_template_node.expression, node_expression
        )

    def test_index_template_node_list_get_view_no_permission(self):
        self._create_test_index()

        response = self._request_test_index_node_list_get_view()
        self.assertEqual(response.status_code, 404)

    def test_index_template_node_list_get_view_with_access(self):
        self._create_test_index()
        self.grant_access(
            obj=self.test_index, permission=permission_document_indexing_edit
        )

        response = self._request_test_index_node_list_get_view()
        self.assertEqual(response.status_code, 200)


class IndexToolsViewTestCase(
    IndexTestMixin, IndexViewTestMixin, IndexToolsViewTestMixin,
    GenericDocumentViewTestCase
):
    def test_indexes_rebuild_no_permission(self):
        self._create_test_index(rebuild=False)

        response = self._request_indexes_rebuild_get_view()
        self.assertNotContains(
            response=response, text=self.test_index.label, status_code=200
        )

        response = self._request_indexes_rebuild_post_view()
        # No error since we just don't see the index
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.test_index.instance_root.get_children_count(), 0
        )

    def test_indexes_rebuild_with_access(self):
        self._create_test_index(rebuild=False)

        self.grant_access(
            obj=self.test_index,
            permission=permission_document_indexing_rebuild
        )

        response = self._request_indexes_rebuild_get_view()
        self.assertContains(
            response=response, text=self.test_index.label, status_code=200
        )

        response = self._request_indexes_rebuild_post_view()
        self.assertEqual(response.status_code, 302)

        # An instance root exists
        self.assertTrue(self.test_index.instance_root.pk)

    def test_indexes_reset_no_permission(self):
        self._create_test_index(rebuild=False)
        self._create_test_index_template_node()
        self.test_index.rebuild()

        response = self._request_indexes_reset_get_view()
        self.assertNotContains(
            response=response, text=self.test_index.label, status_code=200
        )

        response = self._request_indexes_reset_post_view()
        # No error since we just don't see the index
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.test_index.instance_root.get_children_count(), 1
        )

    def test_indexes_reset_with_access(self):
        self._create_test_index(rebuild=False)
        self._create_test_index_template_node()
        self.test_index.rebuild()

        self.grant_access(
            obj=self.test_index,
            permission=permission_document_indexing_rebuild
        )

        response = self._request_indexes_reset_get_view()
        self.assertContains(
            response=response, text=self.test_index.label, status_code=200
        )

        response = self._request_indexes_reset_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            self.test_index.instance_root.get_children_count(), 0
        )
