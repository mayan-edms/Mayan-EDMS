from rest_framework import status

from mayan.apps.documents.permissions import (
    permission_document_type_edit, permission_document_type_view
)
from mayan.apps.documents.tests.mixins import DocumentTestMixin
from mayan.apps.rest_api.tests.base import BaseAPITestCase

from ..models import DocumentTypeMetadataType, MetadataType
from ..permissions import (
    permission_document_metadata_add, permission_document_metadata_edit,
    permission_document_metadata_remove, permission_document_metadata_view,
    permission_metadata_type_create, permission_metadata_type_delete,
    permission_metadata_type_edit, permission_metadata_type_view
)

from .literals import TEST_METADATA_VALUE, TEST_METADATA_VALUE_EDITED
from .mixins import MetadataTypeAPIViewTestMixin, MetadataTypeTestMixin


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
            obj=self.test_metadata_type, permission=permission_metadata_type_delete
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
            obj=self.test_metadata_type, permission=permission_metadata_type_view
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
            obj=self.test_metadata_type, permission=permission_metadata_type_edit
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


class DocumentTypeMetadataTypeAPITestCase(
    DocumentTestMixin, MetadataTypeTestMixin, BaseAPITestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super(DocumentTypeMetadataTypeAPITestCase, self).setUp()
        self._create_test_metadata_type()

    def _create_test_document_type_metadata_type(self):
        self.test_document_type_metadata_type = self.test_document_type.metadata.create(
            metadata_type=self.test_metadata_type, required=False
        )

    def _request_document_type_metadata_type_create_view(self):
        return self.post(
            viewname='rest_api:documenttypemetadatatype-list',
            kwargs={'document_type_pk': self.test_document_type.pk}, data={
                'metadata_type_pk': self.test_metadata_type.pk, 'required': False
            }
        )

    def test_document_type_metadata_type_create_view_no_access(self):
        response = self._request_document_type_metadata_type_create_view()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.test_document_type.metadata.count(), 0)

    def test_document_type_metadata_type_create_view_with_access(self):
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        response = self._request_document_type_metadata_type_create_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        document_type_metadata_type = DocumentTypeMetadataType.objects.first()
        self.assertEqual(response.data['id'], document_type_metadata_type.pk)

    def test_document_type_metadata_type_create_dupicate_view(self):
        self._create_test_document_type_metadata_type()
        self.grant_permission(permission=permission_document_type_edit)
        response = self._request_document_type_metadata_type_create_view()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(list(response.data.keys())[0], 'non_field_errors')

    def _request_document_type_metadata_type_delete_view(self):
        return self.delete(
            viewname='rest_api:documenttypemetadatatype-detail',
            kwargs={
                'document_type_pk': self.test_document_type.pk,
                'metadata_type_pk': self.test_document_type_metadata_type.pk
            }
        )

    def test_document_type_metadata_type_delete_view_no_access(self):
        self._create_test_document_type_metadata_type()

        response = self._request_document_type_metadata_type_delete_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertEqual(self.test_document_type.metadata.count(), 1)

    def test_document_type_metadata_type_delete_view_with_access(self):
        self._create_test_document_type_metadata_type()
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        response = self._request_document_type_metadata_type_delete_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(self.test_document_type.metadata.all().count(), 0)

    def _request_document_type_metadata_type_list_view(self):
        return self.get(
            viewname='rest_api:documenttypemetadatatype-list', kwargs={
                'document_type_pk': self.test_document_type.pk
            }
        )

    def test_document_type_metadata_type_list_view_no_access(self):
        self._create_test_document_type_metadata_type()

        response = self._request_document_type_metadata_type_list_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_document_type_metadata_type_list_view_with_access(self):
        self._create_test_document_type_metadata_type()
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_view
        )

        response = self._request_document_type_metadata_type_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['id'],
            self.test_document_type_metadata_type.pk
        )

    def _request_document_type_metadata_type_edit_view_via_patch(self):
        return self.patch(
            viewname='rest_api:documenttypemetadatatype-detail',
            kwargs={
                'document_type_pk': self.test_document_type.pk,
                'metadata_type_pk': self.test_document_type_metadata_type.pk
            }, data={
                'required': True
            }
        )

    def test_document_type_metadata_type_patch_view_no_access(self):
        self._create_test_document_type_metadata_type()

        response = self._request_document_type_metadata_type_edit_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        document_type_metadata_type = DocumentTypeMetadataType.objects.first()
        self.assertFalse(document_type_metadata_type.required, True)

    def test_document_type_metadata_type_patch_view_with_access(self):
        self._create_test_document_type_metadata_type()
        self.grant_access(
            obj=self.test_document_type,
            permission=permission_document_type_edit
        )

        response = self._request_document_type_metadata_type_edit_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        document_type_metadata_type = DocumentTypeMetadataType.objects.first()
        self.assertEqual(document_type_metadata_type.required, True)

    def _request_document_type_metadata_type_edit_view_via_put(self):
        return self.put(
            viewname='rest_api:documenttypemetadatatype-detail',
            kwargs={
                'document_type_pk': self.test_document_type.pk,
                'metadata_type_pk': self.test_document_type_metadata_type.pk
            }, data={
                'required': True
            }
        )

    def test_document_type_metadata_type_put_view_no_access(self):
        self._create_test_document_type_metadata_type()

        response = self._request_document_type_metadata_type_edit_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        document_type_metadata_type = DocumentTypeMetadataType.objects.first()
        self.assertFalse(document_type_metadata_type.required, True)

    def test_document_type_metadata_type_put_view_with_access(self):
        self._create_test_document_type_metadata_type()
        self.grant_access(
            obj=self.test_document_type, permission=permission_document_type_edit
        )

        response = self._request_document_type_metadata_type_edit_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        document_type_metadata_type = DocumentTypeMetadataType.objects.first()
        self.assertEqual(document_type_metadata_type.required, True)


class DocumentMetadataAPITestMixin:
    def _request_document_metadata_create_view(self):
        return self.post(
            viewname='rest_api:documentmetadata-list',
            kwargs={'document_pk': self.test_document.pk}, data={
                'metadata_type_pk': self.test_metadata_type.pk,
                'value': TEST_METADATA_VALUE
            }
        )

    def _request_document_metadata_delete_view(self):
        return self.delete(
            viewname='rest_api:documentmetadata-detail',
            kwargs={
                'document_pk': self.test_document.pk,
                'metadata_pk': self.test_document_metadata.pk
            }
        )

    def _request_document_metadata_edit_view_via_patch(self):
        return self.patch(
            viewname='rest_api:documentmetadata-detail',
            kwargs={
                'document_pk': self.test_document.pk,
                'metadata_pk': self.test_document_metadata.pk
            }, data={
                'value': TEST_METADATA_VALUE_EDITED
            }
        )

    def _request_document_metadata_edit_view_via_put(self):
        return self.put(
            viewname='rest_api:documentmetadata-detail',
            kwargs={
                'document_pk': self.test_document.pk,
                'metadata_pk': self.test_document_metadata.pk
            }, data={
                'value': TEST_METADATA_VALUE_EDITED
            }
        )

    def _request_document_metadata_list_view(self):
        return self.get(
            viewname='rest_api:documentmetadata-list', kwargs={
                'document_pk': self.test_document.pk
            }
        )


class DocumentMetadataAPITestCase(
    DocumentTestMixin, DocumentMetadataAPITestMixin, MetadataTypeTestMixin,
    BaseAPITestCase
):
    def setUp(self):
        super(DocumentMetadataAPITestCase, self).setUp()
        self._create_test_metadata_type()
        self.test_document_type.metadata.create(
            metadata_type=self.test_metadata_type, required=False
        )

    def _create_document_metadata(self):
        self.test_document_metadata = self.test_document.metadata.create(
            metadata_type=self.test_metadata_type, value=TEST_METADATA_VALUE
        )

    def test_document_metadata_create_view_no_access(self):
        response = self._request_document_metadata_create_view()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.test_document.metadata.count(), 0)

    def test_document_metadata_create_view_with_document_access(self):
        self.grant_access(
            obj=self.test_document, permission=permission_document_metadata_add
        )

        response = self._request_document_metadata_create_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.test_document.metadata.count(), 0)

    def test_document_metadata_create_view_with_metadata_type_access(self):
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_add
        )

        response = self._request_document_metadata_create_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.test_document.metadata.count(), 0)

    def test_document_metadata_create_view_with_full_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_add
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_add
        )

        response = self._request_document_metadata_create_view()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        document_metadata = self.test_document.metadata.first()
        self.assertEqual(response.data['id'], document_metadata.pk)
        self.assertEqual(document_metadata.metadata_type, self.test_metadata_type)
        self.assertEqual(document_metadata.value, TEST_METADATA_VALUE)

    def test_document_metadata_create_duplicate_view(self):
        self._create_document_metadata()
        self.grant_permission(permission=permission_document_metadata_add)

        response = self._request_document_metadata_create_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(list(response.data.keys())[0], 'non_field_errors')

    def test_document_metadata_create_invalid_lookup_value_view(self):
        self.test_metadata_type.lookup = 'invalid,lookup,values,on,purpose'
        self.test_metadata_type.save()
        self.grant_permission(permission=permission_document_metadata_add)

        response = self._request_document_metadata_create_view()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(list(response.data.keys())[0], 'non_field_errors')

    def test_document_metadata_delete_view_no_access(self):
        self._create_document_metadata()

        response = self._request_document_metadata_delete_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.test_document.metadata.all().count(), 1)

    def test_document_metadata_delete_view_with_document_access(self):
        self._create_document_metadata()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_remove
        )

        response = self._request_document_metadata_delete_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.test_document.metadata.all().count(), 1)

    def test_document_metadata_delete_view_with_metadata_type_access(self):
        self._create_document_metadata()
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_remove
        )

        response = self._request_document_metadata_delete_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.test_document.metadata.all().count(), 1)

    def test_document_metadata_delete_view_with_full_access(self):
        self._create_document_metadata()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_remove
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_remove
        )

        response = self._request_document_metadata_delete_view()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.test_document.metadata.all().count(), 0)

    def test_document_metadata_list_view_no_access(self):
        self._create_document_metadata()

        response = self._request_document_metadata_list_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_metadata_list_view_with_document_access(self):
        self._create_document_metadata()

        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_view
        )

        response = self._request_document_metadata_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_document_metadata_list_view_with_metadata_type_access(self):
        self._create_document_metadata()

        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_view
        )

        response = self._request_document_metadata_list_view()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_document_metadata_list_view_with_full_access(self):
        self._create_document_metadata()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_view
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_view
        )

        response = self._request_document_metadata_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['results'][0]['document']['id'], self.test_document.pk
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

    def test_document_metadata_patch_view_no_access(self):
        self._create_document_metadata()

        response = self._request_document_metadata_edit_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document_metadata.refresh_from_db()
        self.assertEqual(self.test_document_metadata.value, TEST_METADATA_VALUE)

    def test_document_metadata_patch_view_document_access(self):
        self._create_document_metadata()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_edit
        )

        response = self._request_document_metadata_edit_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document_metadata.refresh_from_db()
        self.assertEqual(self.test_document_metadata.value, TEST_METADATA_VALUE)

    def test_document_metadata_patch_view_metadata_type_access(self):
        self._create_document_metadata()
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_edit
        )

        response = self._request_document_metadata_edit_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document_metadata.refresh_from_db()
        self.assertEqual(self.test_document_metadata.value, TEST_METADATA_VALUE)

    def test_document_metadata_patch_view_with_full_access(self):
        self._create_document_metadata()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_edit
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_edit
        )

        response = self._request_document_metadata_edit_view_via_patch()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_document_metadata.refresh_from_db()
        self.assertEqual(
            response.data['value'], TEST_METADATA_VALUE_EDITED
        )
        self.assertEqual(
            self.test_document_metadata.value, TEST_METADATA_VALUE_EDITED
        )

    def test_document_metadata_put_view_no_access(self):
        self._create_document_metadata()

        response = self._request_document_metadata_edit_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document_metadata.refresh_from_db()
        self.assertEqual(self.test_document_metadata.value, TEST_METADATA_VALUE)

    def test_document_metadata_put_view_document_access(self):
        self._create_document_metadata()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_edit
        )

        response = self._request_document_metadata_edit_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document_metadata.refresh_from_db()
        self.assertEqual(self.test_document_metadata.value, TEST_METADATA_VALUE)

    def test_document_metadata_put_view_metadata_type_access(self):
        self._create_document_metadata()
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_edit
        )

        response = self._request_document_metadata_edit_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.test_document_metadata.refresh_from_db()
        self.assertEqual(self.test_document_metadata.value, TEST_METADATA_VALUE)

    def test_document_metadata_put_view_with_full_access(self):
        self._create_document_metadata()
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_edit
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_edit
        )

        response = self._request_document_metadata_edit_view_via_put()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test_document_metadata.refresh_from_db()
        self.assertEqual(
            response.data['value'], TEST_METADATA_VALUE_EDITED
        )
        self.assertEqual(
            self.test_document_metadata.value, TEST_METADATA_VALUE_EDITED
        )
