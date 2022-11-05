from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..permissions import permission_index_instance_view

from .literals import TEST_INDEX_TEMPLATE_LABEL
from .mixins import (
    DocumentIndexInstanceViewTestMixin, IndexInstanceTestMixin,
    IndexInstanceViewTestMixin, IndexTemplateTestMixin
)


class DocumentIndexInstanceViewTestCase(
    IndexInstanceTestMixin, DocumentIndexInstanceViewTestMixin,
    IndexTemplateTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        # Create test document after the index template is created.
        self._create_test_document_stub()
        self._populate_test_index_instance_node()

    def test_document_index_instance_list_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_index_instance_list_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_index_instance_list_view_with_index_access(self):
        self.grant_access(
            obj=self._test_index_template,
            permission=permission_index_instance_view
        )

        self._clear_events()

        response = self._request_test_document_index_instance_list_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_index_instance_list_view_with_document_access(self):
        self.grant_access(
            obj=self._test_document,
            permission=permission_index_instance_view
        )

        self._clear_events()

        response = self._request_test_document_index_instance_list_view()
        self.assertNotContains(
            response=response, status_code=200,
            text=TEST_INDEX_TEMPLATE_LABEL
        )
        self.assertContains(
            response=response, status_code=200,
            text=self._test_document.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_index_instance_list_view_with_full_access(self):
        self.grant_access(
            obj=self._test_index_template,
            permission=permission_index_instance_view
        )
        self.grant_access(
            obj=self._test_document,
            permission=permission_index_instance_view
        )

        self._clear_events()

        response = self._request_test_document_index_instance_list_view()
        self.assertContains(
            response=response, status_code=200,
            text=TEST_INDEX_TEMPLATE_LABEL
        )
        self.assertContains(
            response=response, status_code=200,
            text=self._test_document.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_index_list_view_with_full_access(self):
        self.grant_access(
            obj=self._test_index_template,
            permission=permission_index_instance_view
        )
        self.grant_access(
            obj=self._test_document,
            permission=permission_index_instance_view
        )

        self._test_document.delete()

        self._clear_events()

        response = self._request_test_document_index_instance_list_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class IndexInstanceViewTestCase(
    IndexInstanceTestMixin, IndexInstanceViewTestMixin,
    IndexTemplateTestMixin, GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        # Create test document after the index template is created.
        self._create_test_document_stub()
        self._populate_test_index_instance_node()

    def test_index_instance_root_node_view_no_permission(self):
        self._clear_events()

        response = self._request_test_index_instance_node_view(
            index_instance_node=self._test_index_instance_root_node
        )
        self.assertEqual(response.status_code, 403)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_instance_root_node_view_with_access(self):
        self.grant_access(
            obj=self._test_index_template,
            permission=permission_index_instance_view
        )

        self._clear_events()

        response = self._request_test_index_instance_node_view(
            index_instance_node=self._test_index_instance_root_node
        )
        self.assertContains(
            response=response, text=TEST_INDEX_TEMPLATE_LABEL,
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_instance_document_node_view_no_permission(self):
        self._clear_events()

        response = self._request_test_index_instance_node_view(
            index_instance_node=self._test_index_instance_node
        )
        self.assertEqual(response.status_code, 403)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_instance_document_node_view_with_index_access(self):
        self.grant_access(
            obj=self._test_index_template,
            permission=permission_index_instance_view
        )

        self._clear_events()

        response = self._request_test_index_instance_node_view(
            index_instance_node=self._test_index_instance_node
        )
        self.assertContains(
            response=response, text=TEST_INDEX_TEMPLATE_LABEL,
            status_code=200
        )
        self.assertNotContains(
            response=response, text=self._test_document.label,
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_instance_document_node_view_with_document_access(self):
        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_index_instance_node_view(
            index_instance_node=self._test_index_instance_node
        )
        self.assertEqual(response.status_code, 403)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_instance_document_node_view_with_full_access(self):
        self.grant_access(
            obj=self._test_index_template,
            permission=permission_index_instance_view
        )
        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_index_instance_node_view(
            index_instance_node=self._test_index_instance_node
        )
        self.assertContains(
            response=response, text=TEST_INDEX_TEMPLATE_LABEL,
            status_code=200
        )
        self.assertContains(
            response=response, text=self._test_document.label,
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_instance_trashed_document_node_view_with_full_access(self):
        self.grant_access(
            obj=self._test_index_template,
            permission=permission_index_instance_view
        )
        self.grant_access(
            obj=self._test_document, permission=permission_document_view
        )

        self._test_document.delete()

        self._clear_events()

        response = self._request_test_index_instance_node_view(
            index_instance_node=self._test_index_instance_node
        )

        self.assertContains(
            response=response, text=TEST_INDEX_TEMPLATE_LABEL,
            status_code=200
        )
        self.assertNotContains(
            response=response, text=self._test_document.label,
            status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
