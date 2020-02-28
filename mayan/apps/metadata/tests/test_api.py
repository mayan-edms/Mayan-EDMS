from __future__ import unicode_literals

from rest_framework import status

from mayan.apps.documents.permissions import (
    permission_document_type_edit, permission_document_type_view
)
from mayan.apps.documents.tests.mixins import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..models import MetadataType
from ..permissions import (
    permission_metadata_add, permission_metadata_edit,
    permission_metadata_remove, permission_metadata_view,
    permission_metadata_type_create, permission_metadata_type_delete,
    permission_metadata_type_edit, permission_metadata_type_view
)

from .literals import TEST_METADATA_VALUE, TEST_METADATA_VALUE_EDITED
from .mixins import (
    DocumentMetadataAPITestMixin,
    DocumentTypeMetadataTypeRelationAPITestMixin,
    MetadataTypeAPIViewTestMixin,
    MetadataTypeDocumentTypeRelationAPITestMixin, MetadataTypeTestMixin
)


class DocumentMetadataAPITestCase(
    DocumentTestMixin, DocumentMetadataAPITestMixin, MetadataTypeTestMixin,
    BaseAPITestCase
):
    def setUp(self):
        super(DocumentMetadataAPITestCase, self).setUp()
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()

    def _create_test_document_metadata(self):
        self.test_document_metadata = self.test_document.metadata.create(
            metadata_type=self.test_metadata_type, value=TEST_METADATA_VALUE
        )

    def test_document_metadata_create_api_view_no_permission(self):
        metadata_count = self.test_document.metadata.count()
        response = self._request_test_document_metadata_create_api_view()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_document.metadata.count(), metadata_count
        )

    def test_document_metadata_create_api_view_with_document_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_metadata_add
        )
        metadata_count = self.test_document.metadata.count()

        response = self._request_test_document_metadata_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            self.test_document.metadata.count(), metadata_count
        )

    def test_document_metadata_create_api_view_with_metadata_type_access(self):
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_add
        )
        metadata_count = self.test_document.metadata.count()

        response = self._request_test_document_metadata_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_document.metadata.count(), metadata_count
        )

    def test_document_metadata_create_api_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_metadata_add
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_add
        )
        metadata_count = self.test_document.metadata.count()

        response = self._request_test_document_metadata_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            self.test_document.metadata.count(), metadata_count + 1
        )
        document_metadata = self.test_document.metadata.first()
        self.assertEqual(response.data['id'], document_metadata.pk)
        self.assertEqual(
            document_metadata.metadata_type, self.test_metadata_type
        )
        self.assertEqual(document_metadata.value, TEST_METADATA_VALUE)

    def test_document_metadata_create_duplicate_api_view(self):
        self._create_test_document_metadata()
        self.grant_access(
            obj=self.test_document,
            permission=permission_metadata_add
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_add
        )

        response = self._request_test_document_metadata_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(list(response.data.keys())[0], '__all__')

    def test_document_metadata_create_invalid_lookup_value_api_view(self):
        self.test_metadata_type.lookup = 'invalid,lookup,values,on,purpose'
        self.test_metadata_type.save()
        self.grant_access(
            obj=self.test_document,
            permission=permission_metadata_add
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_add
        )

        response = self._request_test_document_metadata_create_api_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(list(response.data.keys())[0], 'value')

    def test_document_metadata_destroy_api_view_no_permission(self):
        self._create_test_document_metadata()
        metadata_count = self.test_document.metadata.count()

        response = self._request_test_document_metadata_destroy_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            self.test_document.metadata.count(), metadata_count
        )

    def test_document_metadata_destroy_api_view_with_document_access(self):
        self._create_test_document_metadata()
        self.grant_access(
            obj=self.test_document,
            permission=permission_metadata_remove
        )
        metadata_count = self.test_document.metadata.count()

        response = self._request_test_document_metadata_destroy_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            self.test_document.metadata.count(), metadata_count
        )

    def test_document_metadata_destroy_api_view_with_metadata_type_access(self):
        self._create_test_document_metadata()
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_remove
        )
        metadata_count = self.test_document.metadata.count()

        response = self._request_test_document_metadata_destroy_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            self.test_document.metadata.count(), metadata_count
        )

    def test_document_metadata_destroy_api_view_with_full_access(self):
        self._create_test_document_metadata()
        self.grant_access(
            obj=self.test_document,
            permission=permission_metadata_remove
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_remove
        )
        metadata_count = self.test_document.metadata.count()

        response = self._request_test_document_metadata_destroy_api_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            self.test_document.metadata.count(), metadata_count - 1
        )

    def test_document_metadata_list_api_view_no_permission(self):
        self._create_test_document_metadata()

        response = self._request_test_document_metadata_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_metadata_list_api_view_with_document_access(self):
        self._create_test_document_metadata()

        self.grant_access(
            obj=self.test_document,
            permission=permission_metadata_view
        )

        response = self._request_test_document_metadata_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_document_metadata_list_api_view_with_metadata_type_access(self):
        self._create_test_document_metadata()

        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_view
        )

        response = self._request_test_document_metadata_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_metadata_list_api_view_with_full_access(self):
        self._create_test_document_metadata()
        self.grant_access(
            obj=self.test_document,
            permission=permission_metadata_view
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_view
        )

        response = self._request_test_document_metadata_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['document']['id'],
            self.test_document.pk
        )
        self.assertEqual(
            response.data['results'][0]['metadata_type']['id'],
            self.test_metadata_type.pk
        )
        self.assertEqual(
            response.data['results'][0]['value'], TEST_METADATA_VALUE
        )
        self.assertEqual(
            response.data['results'][0]['id'], self.test_document_metadata.pk
        )

    def test_document_metadata_partial_update_api_view_no_access(self):
        self._create_test_document_metadata()

        response = self._request_test_document_metadata_partial_update_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document_metadata.refresh_from_db()
        self.assertEqual(
            self.test_document_metadata.value, TEST_METADATA_VALUE
        )

    def test_document_metadata_partial_update_api_view_document_access(self):
        self._create_test_document_metadata()
        self.grant_access(
            obj=self.test_document,
            permission=permission_metadata_edit
        )

        response = self._request_test_document_metadata_partial_update_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document_metadata.refresh_from_db()
        self.assertEqual(
            self.test_document_metadata.value, TEST_METADATA_VALUE
        )

    def test_document_metadata_partial_update_api_view_metadata_type_access(self):
        self._create_test_document_metadata()
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_edit
        )

        response = self._request_test_document_metadata_partial_update_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document_metadata.refresh_from_db()
        self.assertEqual(
            self.test_document_metadata.value, TEST_METADATA_VALUE
        )

    def test_document_metadata_partial_update_api_view_with_full_access(self):
        self._create_test_document_metadata()
        self.grant_access(
            obj=self.test_document,
            permission=permission_metadata_edit
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_edit
        )

        response = self._request_test_document_metadata_partial_update_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_document_metadata.refresh_from_db()
        self.assertEqual(
            response.data['value'], TEST_METADATA_VALUE_EDITED
        )
        self.assertEqual(
            self.test_document_metadata.value, TEST_METADATA_VALUE_EDITED
        )

    def test_document_metadata_put_api_view_no_access(self):
        self._create_test_document_metadata()

        response = self._request_test_document_metadata_update_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document_metadata.refresh_from_db()
        self.assertEqual(
            self.test_document_metadata.value, TEST_METADATA_VALUE
        )

    def test_document_metadata_put_api_view_document_access(self):
        self._create_test_document_metadata()
        self.grant_access(
            obj=self.test_document,
            permission=permission_metadata_edit
        )

        response = self._request_test_document_metadata_update_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document_metadata.refresh_from_db()
        self.assertEqual(
            self.test_document_metadata.value, TEST_METADATA_VALUE
        )

    def test_document_metadata_put_api_view_metadata_type_access(self):
        self._create_test_document_metadata()
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_edit
        )

        response = self._request_test_document_metadata_update_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document_metadata.refresh_from_db()
        self.assertEqual(
            self.test_document_metadata.value, TEST_METADATA_VALUE
        )

    def test_document_metadata_put_api_view_with_full_access(self):
        self._create_test_document_metadata()
        self.grant_access(
            obj=self.test_document,
            permission=permission_metadata_edit
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_edit
        )

        response = self._request_test_document_metadata_update_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_document_metadata.refresh_from_db()
        self.assertEqual(
            response.data['value'], TEST_METADATA_VALUE_EDITED
        )
        self.assertEqual(
            self.test_document_metadata.value, TEST_METADATA_VALUE_EDITED
        )

    def test_document_metadata_retrieve_api_view_no_permission(self):
        self._create_test_document_metadata()

        response = self._request_test_document_metadata_retrieve_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_metadata_retrieve_api_view_document_access(self):
        self._create_test_document_metadata()
        self.grant_access(
            obj=self.test_document,
            permission=permission_metadata_view
        )

        response = self._request_test_document_metadata_retrieve_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_metadata_retrieve_api_view_with_metadata_type_access(self):
        self._create_test_document_metadata()
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_view
        )

        response = self._request_test_document_metadata_retrieve_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_metadata_retrieve_api_view_with_full_access(self):
        self._create_test_document_metadata()
        self.grant_access(
            obj=self.test_document,
            permission=permission_metadata_view
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_view
        )

        response = self._request_test_document_metadata_retrieve_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['document']['id'],
            self.test_document.pk
        )
        self.assertEqual(
            response.data['metadata_type']['id'],
            self.test_metadata_type.pk
        )
        self.assertEqual(
            response.data['id'], self.test_document_metadata.pk
        )
        self.assertEqual(
            response.data['value'], TEST_METADATA_VALUE
        )


class DocumentTypeMetadataTypeRelationAPITestCase(
    DocumentTestMixin, DocumentTypeMetadataTypeRelationAPITestMixin,
    MetadataTypeTestMixin, BaseAPITestCase
):
    auto_upload_document = False

    def setUp(self):
        super(DocumentTypeMetadataTypeRelationAPITestCase, self).setUp()
        self._create_test_metadata_type()

    def test_document_type_metadata_type_relation_create_api_view_no_permission(self):
        relations_count = self.test_document_type.metadata_type_relations.count()

        response = self._request_test_document_type_metadata_type_relation_create_api_view()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_document_type.metadata_type_relations.count(),
            relations_count
        )

    def test_document_type_metadata_type_relation_create_api_view_with_metadata_type_full_access(self):
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )

        relations_count = self.test_document_type.metadata_type_relations.count()

        response = self._request_test_document_type_metadata_type_relation_create_api_view()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_document_type.metadata_type_relations.count(),
            relations_count
        )

    def test_document_type_metadata_type_relation_create_api_view_with_document_type_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        relations_count = self.test_document_type.metadata_type_relations.count()

        response = self._request_test_document_type_metadata_type_relation_create_api_view()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            self.test_document_type.metadata_type_relations.count(),
            relations_count
        )

    def test_document_type_metadata_type_relation_create_api_view_with_full_access(self):
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        relations_count = self.test_document_type.metadata_type_relations.count()

        response = self._request_test_document_type_metadata_type_relation_create_api_view()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            self.test_document_type.metadata_type_relations.count(),
            relations_count + 1
        )

    def test_document_type_metadata_type_relation_destroy_api_view_no_permission(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()
        relations_count = self.test_document_type.metadata_type_relations.count()

        response = self._request_test_document_type_metadata_type_relation_destroy_api_view()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_document_type.metadata_type_relations.count(),
            relations_count
        )

    def test_document_type_metadata_type_relation_destroy_api_view_with_metadata_type_access(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )
        relations_count = self.test_document_type.metadata_type_relations.count()

        response = self._request_test_document_type_metadata_type_relation_destroy_api_view()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_document_type.metadata_type_relations.count(),
            relations_count
        )

    def test_document_type_metadata_type_relation_destroy_api_view_with_document_type_access(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        relations_count = self.test_document_type.metadata_type_relations.count()

        response = self._request_test_document_type_metadata_type_relation_destroy_api_view()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_document_type.metadata_type_relations.count(),
            relations_count
        )

    def test_document_type_metadata_type_relation_destroy_api_view_with_full_access(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )
        relations_count = self.test_document_type.metadata_type_relations.count()

        response = self._request_test_document_type_metadata_type_relation_destroy_api_view()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(
            self.test_document_type.metadata_type_relations.count(),
            relations_count - 1
        )

    def test_document_type_metadata_type_relation_list_api_view_no_permission(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()

        response = self._request_test_document_type_metadata_type_relation_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_type_metadata_type_relation_list_api_view_with_metadata_type_access(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_view
        )

        response = self._request_test_document_type_metadata_type_relation_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_type_metadata_type_relation_list_api_view_with_document_type_access(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_view
        )

        response = self._request_test_document_type_metadata_type_relation_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_document_type_metadata_type_relation_list_api_view_with_full_access(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_view
        )
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_view
        )

        response = self._request_test_document_type_metadata_type_relation_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(
            response.data['results'][0]['id'],
            self.test_document_type_metadata_type_relation.pk
        )

    def test_document_type_metadata_type_relation_partial_update_api_view_no_permission(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()
        required = self.test_document_type.metadata_type_relations.first().required

        response = self._request_test_document_type_metadata_type_relation_partial_update_api_view()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_document_type.metadata_type_relations.first().required,
            required
        )

    def test_document_type_metadata_type_relation_partial_update_api_view_with_metadata_type_access(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )
        required = self.test_document_type.metadata_type_relations.first().required

        response = self._request_test_document_type_metadata_type_relation_partial_update_api_view()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_document_type.metadata_type_relations.first().required,
            required
        )

    def test_document_type_metadata_type_relation_partial_update_api_view_with_document_type_access(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        required = self.test_document_type.metadata_type_relations.first().required

        response = self._request_test_document_type_metadata_type_relation_partial_update_api_view()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_document_type.metadata_type_relations.first().required,
            required
        )

    def test_document_type_metadata_type_relation_partial_update_api_view_with_full_access(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        required = self.test_document_type.metadata_type_relations.first().required

        response = self._request_test_document_type_metadata_type_relation_partial_update_api_view()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertNotEqual(
            self.test_document_type.metadata_type_relations.first().required,
            required
        )

    def test_document_type_metadata_type_relation_retrieve_api_view_no_permission(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()

        response = self._request_test_document_type_metadata_type_relation_retrieve_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_type_metadata_type_relation_retrieve_api_view_with_metadata_type_access(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_view
        )

        response = self._request_test_document_type_metadata_type_relation_retrieve_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_type_metadata_type_relation_retrieve_api_view_with_document_type_access(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_view
        )

        response = self._request_test_document_type_metadata_type_relation_retrieve_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_type_metadata_type_relation_retrieve_api_view_with_full_access(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_view
        )
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_view
        )

        response = self._request_test_document_type_metadata_type_relation_retrieve_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['id'], self.test_document_type_metadata_type_relation.pk
        )

    def test_document_type_metadata_type_relation_update_api_view_no_permission(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()
        required = self.test_document_type.metadata_type_relations.first().required

        response = self._request_test_document_type_metadata_type_relation_update_api_view()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_document_type.metadata_type_relations.first().required,
            required
        )

    def test_document_type_metadata_type_relation_update_api_view_with_metadata_type_access(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )
        required = self.test_document_type.metadata_type_relations.first().required

        response = self._request_test_document_type_metadata_type_relation_update_api_view()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_document_type.metadata_type_relations.first().required,
            required
        )

    def test_document_type_metadata_type_relation_update_api_view_with_document_type_access(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        required = self.test_document_type.metadata_type_relations.first().required

        response = self._request_test_document_type_metadata_type_relation_update_api_view()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_document_type.metadata_type_relations.first().required,
            required
        )

    def test_document_type_metadata_type_relation_update_api_view_with_full_access(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        required = self.test_document_type.metadata_type_relations.first().required

        response = self._request_test_document_type_metadata_type_relation_update_api_view()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertNotEqual(
            self.test_document_type.metadata_type_relations.first().required,
            required
        )


class MetadataTypeAPITestCase(
    MetadataTypeAPIViewTestMixin, MetadataTypeTestMixin, BaseAPITestCase
):
    def test_metadata_type_create_no_permission(self):
        response = self._request_test_metadata_type_create_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(MetadataType.objects.count(), 0)

    def test_metadata_type_create_with_permission(self):
        self.grant_permission(permission=permission_metadata_type_create)
        response = self._request_test_metadata_type_create_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        metadata_type = MetadataType.objects.first()
        self.assertEqual(response.data['id'], metadata_type.pk)

    def test_metadata_type_delete_no_access(self):
        self._create_test_metadata_type()
        response = self._request_test_metadata_type_delete_view()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(MetadataType.objects.count(), 1)

    def test_metadata_type_delete_with_access(self):
        self._create_test_metadata_type()
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_delete
        )

        response = self._request_test_metadata_type_delete_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(MetadataType.objects.count(), 0)

    def test_metadata_type_detail_view_no_access(self):
        self._create_test_metadata_type()

        response = self._request_test_metadata_type_detail_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_metadata_type_detail_view_with_access(self):
        self._create_test_metadata_type()
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_view
        )

        response = self._request_test_metadata_type_detail_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data['label'], self.test_metadata_type.label
        )

    def test_metadata_type_patch_view_no_access(self):
        self._create_test_metadata_type()
        metadata_type_values = self._model_instance_to_dictionary(
            instance=self.test_metadata_type
        )

        response = self._request_test_metadata_type_edit_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_metadata_type.refresh_from_db()
        self.assertEqual(
            self._model_instance_to_dictionary(
                instance=self.test_metadata_type
            ), metadata_type_values
        )

    def test_metadata_type_patch_view_with_access(self):
        self._create_test_metadata_type()
        metadata_type_values = self._model_instance_to_dictionary(
            instance=self.test_metadata_type
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )

        response = self._request_test_metadata_type_edit_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_metadata_type.refresh_from_db()
        self.assertNotEqual(
            self._model_instance_to_dictionary(
                instance=self.test_metadata_type
            ), metadata_type_values
        )

    def test_metadata_type_put_view_no_access(self):
        self._create_test_metadata_type()
        metadata_type_values = self._model_instance_to_dictionary(
            instance=self.test_metadata_type
        )

        response = self._request_test_metadata_type_edit_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_metadata_type.refresh_from_db()
        self.assertEqual(
            self._model_instance_to_dictionary(
                instance=self.test_metadata_type
            ), metadata_type_values
        )

    def test_metadata_type_put_view_with_access(self):
        self._create_test_metadata_type()
        metadata_type_values = self._model_instance_to_dictionary(
            instance=self.test_metadata_type
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )

        response = self._request_test_metadata_type_edit_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_metadata_type.refresh_from_db()
        self.assertNotEqual(
            self._model_instance_to_dictionary(
                instance=self.test_metadata_type
            ), metadata_type_values
        )

    def test_metadata_type_list_view_no_access(self):
        self._create_test_metadata_type()
        response = self._request_test_metadata_type_list_view()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_metadata_type_list_view_with_access(self):
        self._create_test_metadata_type()
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_view
        )

        response = self._request_test_metadata_type_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['label'],
            self.test_metadata_type.label
        )


class MetadataTypeDocumentTypeRelationAPITestCase(
    DocumentTestMixin, MetadataTypeDocumentTypeRelationAPITestMixin,
    MetadataTypeTestMixin, BaseAPITestCase
):
    auto_upload_document = False

    def setUp(self):
        super(MetadataTypeDocumentTypeRelationAPITestCase, self).setUp()
        self._create_test_metadata_type()

    def test_metadata_type_document_type_relation_create_api_view_no_permission(self):
        relations_count = self.test_metadata_type.document_type_relations.count()

        response = self._request_test_metadata_type_document_type_relation_create_api_view()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_metadata_type.document_type_relations.count(),
            relations_count
        )

    def test_metadata_type_document_type_relation_create_api_view_with_document_type_full_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        relations_count = self.test_metadata_type.document_type_relations.count()

        response = self._request_test_metadata_type_document_type_relation_create_api_view()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_metadata_type.document_type_relations.count(),
            relations_count
        )

    def test_metadata_type_document_type_relation_create_api_view_with_metadata_type_access(self):
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )

        relations_count = self.test_metadata_type.document_type_relations.count()

        response = self._request_test_metadata_type_document_type_relation_create_api_view()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            self.test_metadata_type.document_type_relations.count(),
            relations_count
        )

    def test_metadata_type_document_type_relation_create_api_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )

        relations_count = self.test_metadata_type.document_type_relations.count()

        response = self._request_test_metadata_type_document_type_relation_create_api_view()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            self.test_metadata_type.document_type_relations.count(),
            relations_count + 1
        )

    def test_metadata_type_document_type_relation_destroy_api_view_no_permission(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()
        relations_count = self.test_metadata_type.document_type_relations.count()

        response = self._request_test_metadata_type_document_type_relation_destroy_api_view()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_metadata_type.document_type_relations.count(),
            relations_count
        )

    def test_metadata_type_document_type_relation_destroy_api_view_with_document_type_access(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        relations_count = self.test_metadata_type.document_type_relations.count()

        response = self._request_test_metadata_type_document_type_relation_destroy_api_view()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_metadata_type.document_type_relations.count(),
            relations_count
        )

    def test_metadata_type_document_type_relation_destroy_api_view_with_metadata_type_access(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )
        relations_count = self.test_metadata_type.document_type_relations.count()

        response = self._request_test_metadata_type_document_type_relation_destroy_api_view()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_metadata_type.document_type_relations.count(),
            relations_count
        )

    def test_metadata_type_document_type_relation_destroy_api_view_with_full_access(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )
        relations_count = self.test_metadata_type.document_type_relations.count()

        response = self._request_test_metadata_type_document_type_relation_destroy_api_view()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(
            self.test_metadata_type.document_type_relations.count(),
            relations_count - 1
        )

    def test_metadata_type_document_type_relation_list_api_view_no_permission(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()

        response = self._request_test_metadata_type_document_type_relation_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_metadata_type_document_type_relation_list_api_view_with_document_type_access(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_view
        )

        response = self._request_test_metadata_type_document_type_relation_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_metadata_type_document_type_relation_list_api_view_with_metadata_type_access(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_view
        )

        response = self._request_test_metadata_type_document_type_relation_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_metadata_type_document_type_relation_list_api_view_with_full_access(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_view
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_view
        )

        response = self._request_test_metadata_type_document_type_relation_list_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(
            response.data['results'][0]['id'],
            self.test_document_type_metadata_type_relation.pk
        )

    def test_metadata_type_document_type_relation_partial_update_api_view_no_permission(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()
        required = self.test_metadata_type.document_type_relations.first().required

        response = self._request_test_metadata_type_document_type_relation_partial_update_api_view()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_metadata_type.document_type_relations.first().required,
            required
        )

    def test_metadata_type_document_type_relation_partial_update_api_view_with_document_type_access(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        required = self.test_metadata_type.document_type_relations.first().required

        response = self._request_test_metadata_type_document_type_relation_partial_update_api_view()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_metadata_type.document_type_relations.first().required,
            required
        )

    def test_metadata_type_document_type_relation_partial_update_api_view_with_metadata_type_access(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )
        required = self.test_metadata_type.document_type_relations.first().required

        response = self._request_test_metadata_type_document_type_relation_partial_update_api_view()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_metadata_type.document_type_relations.first().required,
            required
        )

    def test_metadata_type_document_type_relation_partial_update_api_view_with_full_access(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )
        required = self.test_metadata_type.document_type_relations.first().required

        response = self._request_test_metadata_type_document_type_relation_partial_update_api_view()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertNotEqual(
            self.test_metadata_type.document_type_relations.first().required,
            required
        )

    def test_metadata_type_document_type_relation_retrieve_api_view_no_permission(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()

        response = self._request_test_metadata_type_document_type_relation_retrieve_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_metadata_type_document_type_relation_retrieve_api_view_with_document_type_access(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_view
        )

        response = self._request_test_metadata_type_document_type_relation_retrieve_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_metadata_type_document_type_relation_retrieve_api_view_with_metadata_type_access(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_view
        )

        response = self._request_test_metadata_type_document_type_relation_retrieve_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_metadata_type_document_type_relation_retrieve_api_view_with_full_access(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_view
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_view
        )

        response = self._request_test_metadata_type_document_type_relation_retrieve_api_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.test_document_type_metadata_type_relation.pk)

    def test_metadata_type_document_type_relation_update_api_view_no_permission(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()
        required = self.test_metadata_type.document_type_relations.first().required

        response = self._request_test_metadata_type_document_type_relation_update_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_metadata_type.document_type_relations.first().required,
            required
        )

    def test_metadata_type_document_type_relation_update_api_view_with_document_type_access(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        required = self.test_metadata_type.document_type_relations.first().required

        response = self._request_test_metadata_type_document_type_relation_update_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_metadata_type.document_type_relations.first().required,
            required
        )

    def test_metadata_type_document_type_relation_update_api_view_with_metadata_type_access(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )
        required = self.test_metadata_type.document_type_relations.first().required

        response = self._request_test_metadata_type_document_type_relation_update_api_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            self.test_metadata_type.document_type_relations.first().required,
            required
        )

    def test_metadata_type_document_type_relation_update_api_view_with_full_access(self):
        self._create_test_metadata_type()
        self._create_test_document_type_metadata_type_relation()
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_metadata_type_edit
        )
        required = self.test_metadata_type.document_type_relations.first().required

        response = self._request_test_metadata_type_document_type_relation_update_api_view()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertNotEqual(
            self.test_metadata_type.document_type_relations.first().required,
            required
        )
