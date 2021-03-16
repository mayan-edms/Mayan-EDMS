from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..permissions import permission_index_instance_view

from .literals import TEST_INDEX_TEMPLATE_LABEL
from .mixins import (
    DocumentIndexInstanceViewTestMixin, IndexInstanceViewTestMixin,
    IndexTemplateTestMixin
)


class DocumentIndexInstanceViewTestCase(
    DocumentIndexInstanceViewTestMixin, IndexTemplateTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_index_template(add_test_document_type=True)
        self._create_test_index_template_node()
        self._create_test_document_stub()

    def test_document_index_instance_list_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_index_instance_list_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_index_instance_list_view_with_index_access(self):
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_instance_view
        )

        self._clear_events()

        response = self._request_test_document_index_instance_list_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_index_instance_list_view_with_document_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_index_instance_view
        )

        self._clear_events()

        response = self._request_test_document_index_instance_list_view()
        self.assertContains(
            count=0, response=response, status_code=200,
            text=TEST_INDEX_TEMPLATE_LABEL
        )
        # 4 instances: title heading, title heading hover, JavaScript
        # document title.
        self.assertContains(
            count=3, response=response, status_code=200,
            text=self.test_document
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_index_instance_list_view_with_full_access(self):
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_instance_view
        )
        self.grant_access(
            obj=self.test_document,
            permission=permission_index_instance_view
        )

        self._clear_events()

        response = self._request_test_document_index_instance_list_view()
        self.assertContains(
            count=1, response=response, status_code=200,
            text=TEST_INDEX_TEMPLATE_LABEL
        )
        # 4 instances: title heading, title heading hover, JavaScript
        # document title, index entry.
        self.assertContains(
            count=5, response=response, status_code=200,
            text=self.test_document
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_index_list_view_with_full_access(self):
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_instance_view
        )
        self.grant_access(
            obj=self.test_document,
            permission=permission_index_instance_view
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_index_instance_list_view()
        self.assertEqual(response.status_code, 404)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class IndexInstanceViewTestCase(
    IndexTemplateTestMixin, IndexInstanceViewTestMixin,
    GenericDocumentViewTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_index_template(add_test_document_type=True)

    def test_index_instance_root_node_view_no_permission(self):
        self._clear_events()

        response = self._request_test_index_instance_node_view(
            index_instance_node=self.test_index_template.instance_root
        )
        self.assertEqual(response.status_code, 403)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_instance_root_node_view_with_access(self):
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_instance_view
        )

        self._clear_events()

        response = self._request_test_index_instance_node_view(
            index_instance_node=self.test_index_template.instance_root
        )
        self.assertContains(
            response=response, text=TEST_INDEX_TEMPLATE_LABEL, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_instance_document_node_view_no_permission(self):
        self._create_test_document_stub()
        self._create_test_index_template_node(
            expression='{{ document.pk }}', rebuild=True
        )

        self._clear_events()

        response = self._request_test_index_instance_node_view(
            index_instance_node=self.test_index_instance_node
        )
        self.assertEqual(response.status_code, 403)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_instance_document_node_view_with_index_access(self):
        self._create_test_document_stub()
        self._create_test_index_template_node(
            expression='{{ document.pk }}', rebuild=True
        )

        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_instance_view
        )

        self._clear_events()

        response = self._request_test_index_instance_node_view(
            index_instance_node=self.test_index_instance_node
        )
        self.assertContains(
            response=response, text=TEST_INDEX_TEMPLATE_LABEL, status_code=200
        )
        self.assertNotContains(
            response=response, text=self.test_document.label, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_instance_document_node_view_with_document_access(self):
        self._create_test_document_stub()
        self._create_test_index_template_node(
            expression='{{ document.pk }}', rebuild=True
        )

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_index_instance_node_view(
            index_instance_node=self.test_index_instance_node
        )
        self.assertEqual(response.status_code, 403)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_instance_document_node_view_with_full_access(self):
        self._create_test_document_stub()
        self._create_test_index_template_node(
            expression='{{ document.pk }}', rebuild=True
        )

        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_instance_view
        )
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_index_instance_node_view(
            index_instance_node=self.test_index_instance_node
        )

        self.assertContains(
            response=response, text=TEST_INDEX_TEMPLATE_LABEL, status_code=200
        )
        self.assertContains(
            response=response, text=self.test_document.label, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_instance_trashed_document_node_view_with_full_access(self):
        self._create_test_document_stub()
        self._create_test_index_template_node(
            expression='{{ document.pk }}', rebuild=True
        )

        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_instance_view
        )
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_index_instance_node_view(
            index_instance_node=self.test_index_instance_node
        )

        self.assertContains(
            response=response, text=TEST_INDEX_TEMPLATE_LABEL, status_code=200
        )
        self.assertNotContains(
            response=response, text=self.test_document.label, status_code=200
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
