from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..models import IndexInstanceNode
from ..permissions import permission_index_template_rebuild

from .mixins import (
    IndexInstanceTestMixin, IndexTemplateTestMixin, IndexToolsViewTestMixin,
    IndexTemplateViewTestMixin
)


class IndexToolsViewTestCase(
    IndexInstanceTestMixin, IndexTemplateTestMixin,
    IndexTemplateViewTestMixin, IndexToolsViewTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_document_stub()
        IndexInstanceNode.objects.exclude(parent=None).delete()

    def test_index_all_rebuild_get_view_no_permission(self):
        index_instance_node_count = self.test_index_instance.get_descendants().count()

        response = self._request_index_all_rebuild_get_view()
        self.assertNotContains(
            response=response, status_code=200,
            text=self.test_index_template.label
        )

        self.assertEqual(
            self.test_index_instance.get_descendants().count(),
            index_instance_node_count
        )

    def test_index_all_rebuild_post_view_no_permission(self):
        index_instance_node_count = self.test_index_instance.get_descendants().count()

        response = self._request_indexes_rebuild_post_view()
        # No error since we just don't see the index.
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.test_index_instance.get_descendants().count(),
            index_instance_node_count
        )

    def test_index_all_rebuild_get_view_with_access(self):
        index_instance_node_count = self.test_index_instance.get_descendants().count()

        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_rebuild
        )

        response = self._request_index_all_rebuild_get_view()
        self.assertContains(
            response=response, status_code=200,
            text=self.test_index_template.label
        )

        self.assertEqual(
            self.test_index_instance.get_descendants().count(),
            index_instance_node_count
        )

    def test_index_all_rebuild_post_view_with_access(self):
        index_instance_node_count = self.test_index_instance.get_descendants().count()

        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_rebuild
        )

        response = self._request_indexes_rebuild_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertNotEqual(
            self.test_index_instance.get_descendants().count(),
            index_instance_node_count
        )

    def test_index_all_reset_get_view_no_permission(self):
        self.test_index_template.rebuild()

        index_instance_node_count = self.test_index_instance.get_descendants().count()

        response = self._request_index_all_reset_get_view()
        self.assertNotContains(
            response=response, status_code=200,
            text=self.test_index_template.label
        )

        self.assertEqual(
            self.test_index_instance.get_descendants().count(),
            index_instance_node_count
        )

    def test_index_all_reset_post_view_no_permission(self):
        self.test_index_template.rebuild()

        index_instance_node_count = self.test_index_instance.get_descendants().count()

        response = self._request_index_all_reset_post_view()
        # No error since we just don't see the index.
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            self.test_index_instance.get_descendants().count(),
            index_instance_node_count
        )

    def test_index_all_reset_get_view_with_access(self):
        self.test_index_template.rebuild()

        index_instance_node_count = self.test_index_instance.get_descendants().count()

        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_rebuild
        )

        response = self._request_index_all_reset_get_view()
        self.assertContains(
            response=response, status_code=200,
            text=self.test_index_template.label
        )

        self.assertEqual(
            self.test_index_instance.get_descendants().count(),
            index_instance_node_count
        )

    def test_index_all_reset_post_view_with_access(self):
        self.test_index_template.rebuild()

        index_instance_node_count = self.test_index_instance.get_descendants().count()

        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_template_rebuild
        )

        response = self._request_index_all_reset_post_view()
        self.assertEqual(response.status_code, 302)

        self.assertNotEqual(
            self.test_index_instance.get_descendants().count(),
            index_instance_node_count
        )
