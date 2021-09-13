from rest_framework import status

from mayan.apps.documents.tests.base import GenericDocumentAPIViewTestCase
from mayan.apps.documents.permissions import permission_document_view

from ..permissions import permission_index_instance_view

from .mixins import (
    DocumentIndexAPIViewTestMixin, IndexInstanceAPIViewTestMixin,
    IndexInstanceNodeAPIViewTestMixin, IndexInstanceTestMixin,
    IndexTemplateTestMixin
)


class DocumentIndexAPIViewTestCase(
    DocumentIndexAPIViewTestMixin, IndexInstanceTestMixin,
    IndexTemplateTestMixin, GenericDocumentAPIViewTestCase
):
    def test_document_index_instance_instance_list_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_document_index_instance_instance_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_index_instance_instance_list_api_view_with_index_access(self):
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_instance_view
        )

        self._clear_events()

        response = self._request_test_document_index_instance_instance_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_index_instance_instance_list_api_view_with_document_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_index_instance_view
        )

        self._clear_events()

        response = self._request_test_document_index_instance_instance_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_document_index_instance_instance_list_api_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_index_instance_view
        )
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_instance_view
        )

        self._clear_events()

        response = self._request_test_document_index_instance_instance_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(
            response.data['results'][0]['id'],
            self.test_index_instance_node.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_index_instance_instance_list_api_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_index_instance_view
        )
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_instance_view
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_document_index_instance_instance_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class IndexInstanceAPIViewTestCase(
    IndexInstanceTestMixin, IndexInstanceAPIViewTestMixin,
    IndexTemplateTestMixin, GenericDocumentAPIViewTestCase
):
    def test_index_instance_detail_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_index_instance_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('id' not in response.data)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_instance_detail_api_view_with_access(self):
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_instance_view
        )

        self._clear_events()

        response = self._request_test_index_instance_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['id'], self.test_index_template.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_instance_list_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_index_instance_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_instance_list_api_view_with_access(self):
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_instance_view
        )

        self._clear_events()

        response = self._request_test_index_instance_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(
            response.data['results'][0]['id'], self.test_index_template.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)


class IndexInstanceNodeAPIViewTestCase(
    IndexInstanceTestMixin, IndexInstanceNodeAPIViewTestMixin,
    IndexTemplateTestMixin, GenericDocumentAPIViewTestCase
):
    def test_index_instance_node_children_list_api_view_no_permissiosn(self):
        self._clear_events()

        response = self._request_test_index_instance_node_children_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_instance_node_children_list_api_view_with_access(self):
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_instance_view
        )

        self._clear_events()

        response = self._request_test_index_instance_node_children_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_instance_node_detail_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_index_instance_node_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('count' not in response.data)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_instance_node_detail_api_view_with_access(self):
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_instance_view
        )

        self._clear_events()

        response = self._request_test_index_instance_node_detail_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['id'], self.test_index_instance_node.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_instance_node_document_list_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_index_instance_node_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('count' not in response.data)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_instance_node_document_list_api_view_with_index_access(self):
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_instance_view
        )

        self._clear_events()

        response = self._request_test_index_instance_node_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_instance_node_document_list_api_view_with_document_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_view
        )

        self._clear_events()

        response = self._request_test_index_instance_node_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('count' not in response.data)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_instance_node_document_list_api_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document_type, permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_instance_view
        )

        self._clear_events()

        response = self._request_test_index_instance_node_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(
            response.data['results'][0]['id'], self.test_document.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_trashed_document_index_instance_node_document_list_api_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document_type, permission=permission_document_view
        )
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_instance_view
        )

        self.test_document.delete()

        self._clear_events()

        response = self._request_test_index_instance_node_document_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_instance_node_list_api_view_no_permission(self):
        self._clear_events()

        response = self._request_test_index_instance_node_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('count' not in response.data)

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)

    def test_index_instance_node_list_api_view_with_access(self):
        self.grant_access(
            obj=self.test_index_template,
            permission=permission_index_instance_view
        )

        self._clear_events()

        response = self._request_test_index_instance_node_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(
            response.data['results'][0]['id'],
            self.test_index_instance_node.pk
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 0)
